use crate::python_wrapper::py_get_python_dir;

#[tauri::command]
pub fn get_python_dir() -> String {
    py_get_python_dir().unwrap()
}