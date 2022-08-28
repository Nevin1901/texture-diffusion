pub mod diffusion_lib;
pub mod python_wrapper;

use diffusion::diffusion_lib::get_python_dir;

#[cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    pyo3::prepare_freethreaded_python();
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .invoke_handler(tauri::generate_handler![get_python_dir])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
