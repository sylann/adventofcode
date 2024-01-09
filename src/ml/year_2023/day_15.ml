let split c s = String.split_on_char c s

module Hash = struct
  type t = int
  type k = string

  let mem : (k, t) Hashtbl.t = Hashtbl.create 50
  let of_char (prev : t) (c : char) : t = (prev + Char.code c) * 17 mod 256
  let of_string (s : k) : t = String.to_bytes s |> Bytes.fold_left of_char 0
  let of_string_mem (s : k) : t = Utils.memoized mem of_string s
end

module Lens = struct
  type t = { label : string; focal : int }

  let same_label a b = a.label = b.label
  let power box_i lens_i lens = (1 + box_i) * (1 + lens_i) * lens.focal
  let to_string lens = Printf.sprintf "[%s %d]" lens.label lens.focal
end

module Op = struct
  type t = Remove of string | Assign of Lens.t

  let parse_remove s =
    match split '-' s with
    | label :: [ "" ] -> Remove label
    | _ -> raise (Invalid_argument "Op.parse_remove expects format '<label>-'")
  ;;

  let parse_assign s =
    match split '=' s with
    | label :: [ num ] -> Assign { label; focal = int_of_string num }
    | _ -> raise (Invalid_argument "Op.parse_assign expects format '<label>=<num>'")
  ;;

  let parse s = s |> if String.ends_with ~suffix:"-" s then parse_remove else parse_assign

  let label_of (op : t) : string =
    match op with
    | Remove label -> label
    | Assign lens -> lens.label
  ;;
end

module Box = struct
  type t = Lens.t list

  let to_string box = box |> List.map Lens.to_string |> String.concat " "
  let _print i box = Printf.printf "Box %d: %s\n" i (to_string box)

  let update (op : Op.t) (box : t) : t =
    match op with
    | Remove label -> box |> List.filter (fun (le : Lens.t) -> le.label <> label)
    | Assign new_lens ->
        let found = ref false in
        let updated =
          box
          |> List.map (fun lens ->
                 if not (Lens.same_label lens new_lens) then lens
                 else begin
                   found := true;
                   new_lens
                 end)
        in
        if not !found then updated @ [ new_lens ] else updated
  ;;
end

let boxes = Array.make 256 []

let _debug_boxes ins box_i : unit =
  Printf.printf "\nAfter \"%s\":  (Target Box:%d)\n" ins box_i;
  boxes |> Array.iteri (fun i box -> if List.length box > 0 then Box._print i box)
;;

let evaluate_ins (ins : string) : unit =
  let op = Op.parse ins in
  let box_i = Hash.of_string_mem (Op.label_of op) in
  boxes.(box_i) <- Box.update op boxes.(box_i);
  (* _debug_boxes ins box_i; *)
  ()
;;

let focus_power () : int =
  let sum f list = List.mapi f list |> List.fold_left ( + ) 0 in
  let box_power i box = box |> sum (Lens.power i) in
  boxes |> Array.to_list |> sum box_power
;;

let solve_1 data = data |> split ',' |> List.map Hash.of_string_mem |> List.fold_left ( + ) 0
let solve_2 data = data |> split ',' |> List.iter evaluate_ins |> focus_power

let () =
  let data = input_line stdin in
  print_endline (string_of_int (solve_1 data));
  print_endline (string_of_int (solve_2 data))
;;
