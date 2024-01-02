open Printf

let rec read_lines ic list =
  match input_line ic with
  | line -> read_lines ic (line :: list)
  | exception End_of_file -> List.rev list

let print_int_list prefix list =
  printf "%s: " prefix;
  List.iter (printf "%d ") list;
  print_newline ()

let print_int_list_list prefix list =
  printf "%s: " prefix;
  List.iter (List.iter (printf "%d ")) list;
  print_newline ()
