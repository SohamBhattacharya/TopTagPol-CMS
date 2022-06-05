import tensorflow as tf
from tensorflow import keras

from classification_models.tfkeras import Classifiers

#from tensorflow.keras import mixed_precision
#policy = mixed_precision.Policy("mixed_float16")
#mixed_precision.set_global_policy(policy)

# A shape is (N, P_A, C), B shape is (N, P_B, C)
# D shape is (N, P_A, P_B)
def batch_distance_matrix_general(A, B):
    with tf.name_scope('dmat'):
        r_A = tf.reduce_sum(A * A, axis=2, keepdims=True)
        r_B = tf.reduce_sum(B * B, axis=2, keepdims=True)
        m = tf.matmul(A, tf.transpose(B, perm=(0, 2, 1)))
        D = r_A - 2 * m + tf.transpose(r_B, perm=(0, 2, 1))
        return D


def knn(num_points, k, topk_indices, features):
    # topk_indices: (N, P, K)
    # features: (N, P, C)
    with tf.name_scope('knn'):
        queries_shape = tf.shape(features)
        batch_size = queries_shape[0]
        batch_indices = tf.tile(tf.reshape(tf.range(batch_size), (-1, 1, 1, 1)), (1, num_points, k, 1))
        indices = tf.concat([batch_indices, tf.expand_dims(topk_indices, axis=3)], axis=3)  # (N, P, K, 2)
        return tf.gather_nd(features, indices)


def edge_conv(points, features, num_points, K, channels, with_bn=True, activation='relu', pooling='average', name='edgeconv'):
    """EdgeConv
    Args:
        K: int, number of neighbors
        in_channels: # of input channels
        channels: tuple of output channels
        pooling: pooling method ('max' or 'average')
    Inputs:
        points: (N, P, C_p)
        features: (N, P, C_0)
    Returns:
        transformed points: (N, P, C_out), C_out = channels[-1]
    """

    with tf.name_scope('edgeconv'):

        # distance
        D = batch_distance_matrix_general(points, points)  # (N, P, P)
        _, indices = tf.nn.top_k(-D, k=K + 1)  # (N, P, K+1)
        indices = indices[:, :, 1:]  # (N, P, K)

        fts = features
        knn_fts = knn(num_points, K, indices, fts)  # (N, P, K, C)
        knn_fts_center = tf.tile(tf.expand_dims(fts, axis=2), (1, 1, K, 1))  # (N, P, K, C)
        knn_fts = tf.concat([knn_fts_center, tf.subtract(knn_fts, knn_fts_center)], axis=-1)  # (N, P, K, 2*C)

        x = knn_fts
        for idx, channel in enumerate(channels):
            x = keras.layers.Conv2D(channel, kernel_size=(1, 1), strides=1, data_format='channels_last',
                                    use_bias=False if with_bn else True, kernel_initializer='glorot_normal', name='%s_conv%d' % (name, idx))(x)
            if with_bn:
                x = keras.layers.BatchNormalization(name='%s_bn%d' % (name, idx))(x)
            if activation:
                x = keras.layers.Activation(activation, name='%s_act%d' % (name, idx))(x)

        if pooling == 'max':
            fts = tf.reduce_max(x, axis=2)  # (N, P, C')
        else:
            fts = tf.reduce_mean(x, axis=2)  # (N, P, C')

        # shortcut
        sc = keras.layers.Conv2D(channels[-1], kernel_size=(1, 1), strides=1, data_format='channels_last',
                                 use_bias=False if with_bn else True, kernel_initializer='glorot_normal', name='%s_sc_conv' % name)(tf.expand_dims(features, axis=2))
        if with_bn:
            sc = keras.layers.BatchNormalization(name='%s_sc_bn' % name)(sc)
        sc = tf.squeeze(sc, axis=2)

        if activation:
            return keras.layers.Activation(activation, name='%s_sc_act' % name)(sc + fts)  # (N, P, C')
        else:
            return sc + fts


def _particle_net_base(points, features=None, mask=None, setting=None, name='particle_net'):
    # points : (N, P, C_coord)
    # features:  (N, P, C_features), optional
    # mask: (N, P, 1), optinal

    with tf.name_scope(name):
        if features is None:
            features = points

        if mask is not None:
            mask = tf.cast(tf.not_equal(mask, 0), dtype='float32')  # 1 if valid
            coord_shift = tf.multiply(999., tf.cast(tf.equal(mask, 0), dtype='float32'))  # make non-valid positions to 99

        fts = tf.squeeze(keras.layers.BatchNormalization(name='%s_fts_bn' % name)(tf.expand_dims(features, axis=2)), axis=2)
        for layer_idx, layer_param in enumerate(setting.conv_params):
            K, channels = layer_param
            pts = tf.add(coord_shift, points) if layer_idx == 0 else tf.add(coord_shift, fts)
            fts = edge_conv(pts, fts, setting.num_points, K, channels, with_bn=True, activation='relu',
                            pooling=setting.conv_pooling, name='%s_%s%d' % (name, 'EdgeConv', layer_idx))

        if mask is not None:
            fts = tf.multiply(fts, mask)

        pool = tf.reduce_mean(fts, axis=1)  # (N, C)

        if setting.fc_params is not None:
            x = pool
            for layer_idx, layer_param in enumerate(setting.fc_params):
                units, drop_rate = layer_param
                x = keras.layers.BatchNormalization(name='dense_bn%d' % (layer_idx))(x)
                x = keras.layers.Dense(units, activation='relu')(x)
                if drop_rate is not None and drop_rate > 0:
                    x = keras.layers.Dropout(drop_rate)(x)
            
            if (setting.num_class is not None) :
                out = keras.layers.Dense(setting.num_class, activation='softmax')(x)
                return out  # (N, num_classes)
            else :
                return x #(N, units)
        else:
            return pool


def _particle_net_base_mod1(points, features=None, mask=None, svFeatures=None, svMask = None, jetFeatures=None, setting=None, name='particle_net'):
    # points : (N, P, C_coord)
    # features:  (N, P, C_features), optional
    # mask: (N, P, 1), optinal

    with tf.name_scope(name):
        if features is None:
            features = points

        if mask is not None:
            mask = tf.cast(tf.not_equal(mask, 0), dtype='float32')  # 1 if valid
            coord_shift = tf.multiply(999., tf.cast(tf.equal(mask, 0), dtype='float32'))  # make non-valid positions to 99

        fts = tf.squeeze(keras.layers.BatchNormalization(name='%s_fts_bn' % name)(tf.expand_dims(features, axis=2)), axis=2)
        for layer_idx, layer_param in enumerate(setting.conv_params):
            K, channels = layer_param
            pts = tf.add(coord_shift, points) if layer_idx == 0 else tf.add(coord_shift, fts)
            fts = edge_conv(pts, fts, setting.num_points, K, channels, with_bn=True, activation='relu',
                            pooling=setting.conv_pooling, name='%s_%s%d' % (name, 'EdgeConv', layer_idx))

        if mask is not None:
            fts = tf.multiply(fts, mask)

        pool = tf.reduce_mean(fts, axis=1)  # (N, C)
        
        if setting.fc_params is not None:
            x = pool
            
            nSVoutput = 0
            
            if (svFeatures is not None) :
                
                resnet, preproc = Classifiers.get("resnet1d50")
                
                sv_output = resnet(
                    #input_shape = input_shape,
                    input_tensor = svFeatures,
                    mask_tensor = svMask,
                    include_top = False,
                    #classes = nCategory
                ).output
                
                sv_output = keras.layers.GlobalAveragePooling1D()(sv_output)
                sv_output = keras.layers.BatchNormalization(name='sv_bn')(sv_output)
                sv_output = keras.layers.Dense(setting.sv_fc_units, activation='relu')(sv_output)
                
                nSVoutput = setting.sv_fc_units
                
                x = tf.keras.layers.Concatenate(axis = 1)([x, sv_output])
            
            nJetFeatures = 0
            
            if (jetFeatures is not None) :
                
                nJetFeatures = jetFeatures.shape[1]
                x = tf.keras.layers.Concatenate(axis = 1)([x, jetFeatures])
            
            nNodeExtra = nSVoutput + nJetFeatures
            
            for layer_idx, layer_param in enumerate(setting.fc_params):
                units, drop_rate = layer_param
                
                units += nNodeExtra
                
                x = keras.layers.BatchNormalization(name='dense_bn%d' % (layer_idx))(x)
                
                x = keras.layers.Dense(units, activation='relu')(x)
                if drop_rate is not None and drop_rate > 0:
                    x = keras.layers.Dropout(drop_rate)(x)
            out = keras.layers.Dense(setting.num_class, activation='softmax')(x)
            return out  # (N, num_classes)
        else:
            return pool


class _DotDict:
    pass


def get_particle_net(num_classes, input_shapes):
    r"""ParticleNet model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting = _DotDict()
    setting.num_class = num_classes
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting.conv_params = [
        (16, (64, 64, 64)),
        (16, (128, 128, 128)),
        (16, (256, 256, 256)),
        ]
    # conv_pooling: 'average' or 'max'
    setting.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting.fc_params = [(256, 0.1)]
    setting.num_points = input_shapes['points'][0]

    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    outputs = _particle_net_base(points, features, mask, setting, name='ParticleNet')

    return keras.Model(inputs=[points, features, mask], outputs=outputs, name='ParticleNet')


def get_particle_net_lite(num_classes, input_shapes):
    r"""ParticleNet-Lite model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting = _DotDict()
    setting.num_class = num_classes
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting.conv_params = [
        (7, (32, 32, 32)),
        (7, (64, 64, 64)),
        ]
    # conv_pooling: 'average' or 'max'
    setting.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting.fc_params = [(128, 0.1)]
    setting.num_points = input_shapes['points'][0]

    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    outputs = _particle_net_base(points, features, mask, setting, name='ParticleNet')

    return keras.Model(inputs=[points, features, mask], outputs=outputs, name='ParticleNet')


def get_particle_net_mod1(num_classes, input_shapes):
    r"""ParticleNet model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting = _DotDict()
    setting.num_class = num_classes
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting.conv_params = [
        (64, (64, 64, 64)),
        (64, (128, 128, 128)),
        (64, (256, 256, 256)),
        ]
    # conv_pooling: 'average' or 'max'
    setting.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting.fc_params = [(512, 0.1)]
    setting.num_points = input_shapes['points'][0]
    
    setting.sv_fc_units = 512

    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    
    svFeatures = keras.Input(name='svFeatures', shape=input_shapes['svFeatures']) if 'svFeatures' in input_shapes else None
    svMask = keras.Input(name='svMask', shape=input_shapes['svMask']) if 'svMask' in input_shapes else None
    
    jetFeatures = keras.Input(name='jetFeatures', shape=input_shapes['jetFeatures']) if 'jetFeatures' in input_shapes else None
    
    outputs = _particle_net_base_mod1(
        points = points,
        features = features,
        mask = mask,
        svFeatures = svFeatures,
        svMask = svMask,
        jetFeatures = jetFeatures,
        setting = setting,
        name = 'ParticleNet'
    )
    
    inputs = [points, features, mask]
    
    for inp in [svFeatures, svMask, jetFeatures] :
        
        if (inp is not None) :
            
            inputs.append(inp)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='ParticleNet')


def get_particle_net_mod1a(num_classes, input_shapes):
    r"""ParticleNet model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting = _DotDict()
    setting.num_class = num_classes
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting.conv_params = [
        (64, (64, 64, 64)),
        (64, (128, 128, 128)),
        (64, (256, 256, 256)),
        ]
    # conv_pooling: 'average' or 'max'
    setting.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting.fc_params = [(512, 0.2)]
    setting.num_points = input_shapes['points'][0]
    
    setting.sv_fc_units = 512

    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    
    svFeatures = keras.Input(name='svFeatures', shape=input_shapes['svFeatures']) if 'svFeatures' in input_shapes else None
    svMask = keras.Input(name='svMask', shape=input_shapes['svMask']) if 'svMask' in input_shapes else None
    
    jetFeatures = keras.Input(name='jetFeatures', shape=input_shapes['jetFeatures']) if 'jetFeatures' in input_shapes else None
    
    outputs = _particle_net_base_mod1(
        points = points,
        features = features,
        mask = mask,
        svFeatures = svFeatures,
        svMask = svMask,
        jetFeatures = jetFeatures,
        setting = setting,
        name = 'ParticleNet'
    )
    
    inputs = [points, features, mask]
    
    for inp in [svFeatures, svMask, jetFeatures] :
        
        if (inp is not None) :
            
            inputs.append(inp)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='ParticleNet')


def get_particle_net_mod1b(num_classes, input_shapes, nn_part = 64, layer1ch_part = 64, layer1ch_sv = 32):
    r"""ParticleNet model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting_part = _DotDict()
    setting_part.num_class = None
    setting_part.num_points = input_shapes['points'][0]
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting_part.conv_params = [
        (nn_part, (layer1ch_part*1, layer1ch_part*1, layer1ch_part*1)),
        (nn_part, (layer1ch_part*2, layer1ch_part*2, layer1ch_part*2)),
        (nn_part, (layer1ch_part*4, layer1ch_part*4, layer1ch_part*4)),
        ]
    # conv_pooling: 'average' or 'max'
    setting_part.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting_part.fc_params = None
    #setting_part.fc_params = [(256, 0.2)]
    
    
    nsv = input_shapes['svFeatures'][0]
    
    setting_sv = _DotDict()
    setting_sv.num_class = None
    setting_sv.num_points = input_shapes['svPoints'][0]
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting_sv.conv_params = [
        (setting_sv.num_points-1, (layer1ch_sv*1, layer1ch_sv*1, layer1ch_sv*1)),
        (setting_sv.num_points-1, (layer1ch_sv*2, layer1ch_sv*2, layer1ch_sv*2)),
        (setting_sv.num_points-1, (layer1ch_sv*4, layer1ch_sv*4, layer1ch_sv*4)),
        ]
    # conv_pooling: 'average' or 'max'
    setting_sv.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting_sv.fc_params = None
    #setting_sv.fc_params = [(128, 0.2)]
    
    
    fc_params = [(512, 0.2)]
    
    
    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    
    svPoints = keras.Input(name='svPoints', shape=input_shapes['svPoints'])
    svFeatures = keras.Input(name='svFeatures', shape=input_shapes['svFeatures']) if 'svFeatures' in input_shapes else None
    svMask = keras.Input(name='svMask', shape=input_shapes['svMask']) if 'svMask' in input_shapes else None
    
    jetFeatures = keras.Input(name='jetFeatures', shape=input_shapes['jetFeatures']) if 'jetFeatures' in input_shapes else None
    
    
    output_part = _particle_net_base(
        points = points,
        features = features,
        mask = mask,
        setting = setting_part,
        name = 'ParticleNet_consti'
    )
    
    output_sv = _particle_net_base(
        points = svPoints,
        features = svFeatures,
        mask = svMask,
        setting = setting_sv,
        name = 'ParticleNet_sv'
    )
    
    
    # Catenate and pass to dense network
    l_features = [output_part, output_sv]
    
    if (jetFeatures is not None) :
        
        l_features.append(jetFeatures)
    
    x = tf.keras.layers.Concatenate(axis = 1)(l_features)
    
    for layer_idx, layer_param in enumerate(fc_params):
        units, drop_rate = layer_param
        
        x = keras.layers.BatchNormalization(name='dense_bn%d' % (layer_idx))(x)
        
        x = keras.layers.Dense(units, activation='relu')(x)
        if drop_rate is not None and drop_rate > 0:
            x = keras.layers.Dropout(drop_rate)(x)
    
    outputs = keras.layers.Dense(num_classes, activation='softmax')(x)
    
    
    inputs = [points, features, mask, svPoints, svFeatures, svMask, jetFeatures]
    
    #for inp in [svPoints, svFeatures, svMask, jetFeatures] :
    #    
    #    if (inp is not None) :
    #        
    #        inputs.append(inp)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='ParticleNet')


def get_particle_net_mod1c(num_classes, input_shapes) :
    
    return get_particle_net_mod1b(
        num_classes,
        input_shapes,
        nn_part = 32,
        layer1ch_part = 32,
        layer1ch_sv = 16,
    )

def get_particle_net_mod1d(num_classes, input_shapes) :
    
    return get_particle_net_mod1b(
        num_classes,
        input_shapes,
        nn_part = 16,
        layer1ch_part = 16,
        layer1ch_sv = 16,
    )


def get_particle_net_mod2(num_classes, input_shapes):
    r"""ParticleNet model from `"ParticleNet: Jet Tagging via Particle Clouds"
    <https://arxiv.org/abs/1902.08570>`_ paper.
    Parameters
    ----------
    num_classes : int
        Number of output classes.
    input_shapes : dict
        The shapes of each input (`points`, `features`, `mask`).
    """
    setting = _DotDict()
    setting.num_class = num_classes
    # conv_params: list of tuple in the format (K, (C1, C2, C3))
    setting.conv_params = [
        (64, (64, 64, 64)),
        (64, (128, 128, 128)),
        #(64, (128, 128, 128)),
        (64, (256, 256, 256)),
        ]
    # conv_pooling: 'average' or 'max'
    setting.conv_pooling = 'average'
    # fc_params: list of tuples in the format (C, drop_rate)
    setting.fc_params = [(512, 0.1), (512, 0.1), (512, 0.1)]
    setting.num_points = input_shapes['points'][0]

    points = keras.Input(name='points', shape=input_shapes['points'])
    features = keras.Input(name='features', shape=input_shapes['features']) if 'features' in input_shapes else None
    mask = keras.Input(name='mask', shape=input_shapes['mask']) if 'mask' in input_shapes else None
    jetFeatures = keras.Input(name='jetFeatures', shape=input_shapes['jetFeatures']) if 'jetFeatures' in input_shapes else None
    outputs = _particle_net_base_mod1(points, features, mask, jetFeatures, setting, name='ParticleNet')

    inputs = [points, features, mask]
    
    if (jetFeatures is not None) :
        
        inputs.append(jetFeatures)
    
    return keras.Model(inputs=inputs, outputs=outputs, name='ParticleNet')
