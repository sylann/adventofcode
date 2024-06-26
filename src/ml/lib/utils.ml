open Printf

let ( => ) a b = Seq.init (b - a) (fun i -> i)

let rec read_lines ic list =
  match input_line ic with
  | line -> read_lines ic (line :: list)
  | exception End_of_file -> List.rev list
;;

let print_list ?(prefix = "") fmt (list : 'a list) =
  if prefix != "" then printf "%s" prefix;
  list |> List.iter @@ printf fmt;
  print_newline ()
;;

let print_list_list ?(prefix = "") fmt (list : 'a list list) =
  if prefix != "" then printf "%s" prefix;
  list |> List.iter @@ List.iter @@ printf fmt;
  print_newline ()
;;

module Array = struct
  include Array

  let sum f arr = Array.fold_left (fun acc x -> acc + f x) 0 arr
  let count f arr = arr |> Array.to_seq |> Seq.filter f |> Seq.length
end

module Dir = struct
  type t = Up | Down | Left | Right

  let to_string (d : t) : string =
    match d with
    | Up -> "^"
    | Down -> "v"
    | Left -> "<"
    | Right -> ">"
  ;;

  let _print (d : t) : unit = Printf.printf "%s" (to_string d)
end

module Vec2 = struct
  type t = { x : int; y : int }

  let next (d : Dir.t) (pos : t) : t =
    match d with
    | Up -> { x = pos.x; y = pos.y - 1 }
    | Down -> { x = pos.x; y = pos.y + 1 }
    | Left -> { x = pos.x - 1; y = pos.y }
    | Right -> { x = pos.x + 1; y = pos.y }
  ;;
end

module Row = struct
  type t = char array

  let of_string (s : string) : t = s |> String.to_seq |> Array.of_seq
  let to_string (a : t) : string = a |> Array.to_seq |> String.of_seq
  let print (r : t) : unit = printf "%s" (to_string r)
end

module Grid = struct
  type t = Row.t array

  let size (g : t) : int * int = (Array.length g, Array.length g.(0))
  let of_string_list (sl : string list) : t = sl |> List.map Row.of_string |> Array.of_list
  let to_string_list (g : t) : string list = g |> Array.map Row.to_string |> Array.to_list
  let of_string (s : string) : t = s |> String.split_on_char '\n' |> of_string_list
  let to_string (g : t) : string = g |> to_string_list |> String.concat "\n"
  let print (g : t) : unit = print_endline (to_string g)
end

let memoized tbl (f : 'a -> 'b) (key : 'a) =
  match Hashtbl.find_opt tbl key with
  | Some out -> out
  | None ->
      let out = f key in
      Hashtbl.add tbl key out;
      out
;;
