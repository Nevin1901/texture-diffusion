import test_rust

try:
    test_rust.start_server()
except KeyboardInterrupt:
    quit()
