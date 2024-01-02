let parse_nums line = List.map int_of_string (String.split_on_char ' ' line)

let rec compute_deltas nums deltas =
  match nums with
  | [] | _ :: [] -> List.rev deltas
  | a :: b :: rest -> compute_deltas (b :: rest) (b - a :: deltas)

let rec extrapolate nums fold_left =
  let deltas = compute_deltas nums [] in
  let prev = if fold_left then List.hd nums else List.hd (List.rev nums) in
  let sign = if fold_left then -1 else 1 in

  let is_0 n = n = 0 in
  match List.for_all is_0 deltas with
  | true -> prev
  | false -> prev + (sign * extrapolate deltas fold_left)

let rec count data total fold_left =
  match data with
  | [] -> total
  | line :: rest ->
      let total = total + extrapolate (parse_nums line) fold_left in
      count rest (total) fold_left

let solve_1 data = count data 0 false
let solve_2 data = count data 0 true

let () =
  let data = Utils.read_lines stdin [] in
  print_endline (string_of_int (solve_1 data));
  print_endline (string_of_int (solve_2 data));
