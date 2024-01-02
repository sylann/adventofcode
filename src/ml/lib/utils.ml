open Printf

let rec read_lines ic list =
  match input_line ic with
  | line -> read_lines ic (line :: list)
  | exception End_of_file -> List.rev list
