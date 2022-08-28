use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    fs::read_to_string
};

use pyo3::prelude::*;

// fn test_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(start_server, m)?)?;
//     Ok(())
// }

fn start_server() {
    println!("starting server");
    let python_dir = get_python_dir().unwrap();
    println!("{}", python_dir);
    println!("done");

    let html = read_to_string("/home/nevin/Desktop/texture-dream/texture-diffusion/rust-framework/src/template.html").unwrap();
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("connection established");

        handle_connection(stream, &html);
    }
    println!("Hello, world!");
}

fn get_python_dir() -> PyResult<String> {
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let executable: String = sys.getattr("executable")?.extract()?;

        Ok(executable)
    })
}

fn handle_connection(mut stream: TcpStream, template: &str) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let len = template.len();

    let response = format!("HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}", len, template);

    stream.write_all(response.as_bytes()).unwrap();

    // println!("{:#?}", http_request);
}

mod tests {
    use crate::start_server;
    use pyo3::prelude::*;

    #[test]
    fn start() {
        pyo3::prepare_freethreaded_python();
        start_server();
    }
}
