# Description:
# TensorBoard plugin for precision-recall curves.

load("//tensorboard/defs:protos.bzl", "tb_proto_library")

package(default_visibility = ["//tensorboard:internal"])

licenses(["notice"])

py_library(
    name = "metadata",
    srcs = ["metadata.py"],
    srcs_version = "PY3",
    deps = [
        ":protos_all_py_pb2",
        "//tensorboard/compat/proto:protos_all_py_pb2",
    ],
)

py_library(
    name = "my_pr_curves_plugin",
    srcs = ["my_pr_curves_plugin.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        ":metadata",
        "//tensorboard:expect_numpy_installed",
        "//tensorboard:plugin_util",
        "//tensorboard/backend:http_util",
        "//tensorboard/data:provider",
        "//tensorboard/plugins:base_plugin",
        "@org_pocoo_werkzeug",
    ],
)

py_test(
    name = "my_pr_curves_plugin_test",
    size = "medium",  # tf integration test
    srcs = ["my_pr_curves_plugin_test.py"],
    srcs_version = "PY3",
    deps = [
        ":metadata",
        ":pr_curve_demo_lib",
        ":my_pr_curves_plugin",
        "//tensorboard:context",
        "//tensorboard:expect_numpy_installed",
        "//tensorboard:expect_tensorflow_installed",
        "//tensorboard/backend/event_processing:data_provider",
        "//tensorboard/backend/event_processing:event_multiplexer",
        "//tensorboard/plugins:base_plugin",
        "@org_pocoo_werkzeug",
    ],
)

# TODO(#2007): Remove this after pruning unnecessary TensorFlow deps in main test
py_test(
    name = "my_pr_curves_plugin_notf_test",
    size = "medium",  # tf integration test
    srcs = ["my_pr_curves_plugin_test.py"],
    main = "my_pr_curves_plugin_test.py",
    srcs_version = "PY3",
    deps = [
        ":metadata",
        ":pr_curve_demo_lib",
        ":my_pr_curves_plugin",
        "//tensorboard:context",
        "//tensorboard:expect_numpy_installed",
        "//tensorboard:expect_tensorflow_installed",
        "//tensorboard/backend/event_processing:data_provider",
        "//tensorboard/backend/event_processing:event_multiplexer",
        "//tensorboard/compat:no_tensorflow",
        "//tensorboard/plugins:base_plugin",
        "@org_pocoo_werkzeug",
    ],
)

py_library(
    name = "summary",
    srcs = ["summary.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        ":metadata",
        "//tensorboard:expect_numpy_installed",
        "//tensorboard:expect_tensorflow_installed",
        "//tensorboard/util:tensor_util",
    ],
)

py_test(
    name = "summary_test",
    size = "small",
    srcs = ["summary_test.py"],
    srcs_version = "PY3",
    deps = [
        ":summary",
        "//tensorboard:expect_numpy_installed",
        "//tensorboard:expect_tensorflow_installed",
        "//tensorboard/compat/proto:protos_all_py_pb2",
        "//tensorboard/plugins:base_plugin",
        "//tensorboard/util:test_util",
        "@org_pocoo_werkzeug",
    ],
)

tb_proto_library(
    name = "protos_all",
    srcs = ["plugin_data.proto"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "pr_curve_demo",
    srcs = ["pr_curve_demo.py"],
    srcs_version = "PY3",
    deps = [":pr_curve_demo_lib"],
)

py_library(
    name = "pr_curve_demo_lib",
    srcs = ["pr_curve_demo.py"],
    srcs_version = "PY3",
    deps = [
        ":summary",
        "//tensorboard:expect_tensorflow_installed",
    ],
)
