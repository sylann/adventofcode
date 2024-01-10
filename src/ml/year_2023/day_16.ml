open Utils

module Dir = struct
  include Dir

  let next (d : t) (c : char) : t list =
    match (d, c) with
    | d, '.' -> [ d ]
    | Up, '\\' -> [ Left ]
    | Down, '\\' -> [ Right ]
    | Left, '\\' -> [ Up ]
    | Right, '\\' -> [ Down ]
    | Up, '/' -> [ Right ]
    | Down, '/' -> [ Left ]
    | Left, '/' -> [ Down ]
    | Right, '/' -> [ Up ]
    | Up, '|' -> [ Up ]
    | Down, '|' -> [ Down ]
    | Left, '|' -> [ Up; Down ]
    | Right, '|' -> [ Up; Down ]
    | Up, '-' -> [ Left; Right ]
    | Down, '-' -> [ Left; Right ]
    | Left, '-' -> [ Left ]
    | Right, '-' -> [ Right ]
    | _ -> raise (Invalid_argument "Unexpected case in Dir.next")
  ;;
end

type beams = Dir.t list
type beams_grid = beams array array

let _show_beams (g : Grid.t) (bg : beams_grid) =
  Printf.printf "\nBeams grid:\n";
  g
  |> Array.iteri (fun y row ->
         row
         |> Array.iteri (fun x c ->
                let beams = bg.(y).(x) in
                let n = List.length beams in
                if c <> '.' || n = 0 then Printf.printf "%c" c
                else if n = 1 then Dir._print (List.hd beams)
                else Printf.printf "%d" n);
         Printf.printf "\n");
  Printf.printf "%!"
;;

let _show_energy g bg =
  Printf.printf "\nEnergy grid:\n";
  g
  |> Array.iteri (fun y row ->
         row
         |> Array.iteri (fun x c ->
                if List.length bg.(y).(x) > 0 then Printf.printf "#" else Printf.printf "%c" c);
         Printf.printf "\n");
  Printf.printf "%!"
;;

let simulate_beams (g : Grid.t) ~(dir0 : Dir.t) ~(pos0 : Vec2.t) : beams_grid =
  let w, h = Grid.size g in
  let bg : beams_grid = Array.make_matrix w h [] in

  let out_of_bound ({ x; y }: Vec2.t) = x < 0 || x > w-1 || y < 0 || y > h-1 in
  let seen = Hashtbl.create 200 in

  let rec walk_beam (dir : Dir.t) (pos : Vec2.t) : unit =
    if out_of_bound pos then ()
    else
      match Hashtbl.find_opt seen (dir, pos) with
      | Some _ -> ()
      | None -> begin
          Hashtbl.add seen (dir, pos) ();
          let cell = g.(pos.y).(pos.x) in
          bg.(pos.y).(pos.x) <- dir :: bg.(pos.y).(pos.x);
          Dir.next dir cell |> List.iter (fun nd -> walk_beam nd (Vec2.next nd pos))
        end
  in

  walk_beam dir0 pos0;

  (* _show_beams g bg;
     _show_energy g bg; *)
  bg
;;

let count_energized (bg : beams_grid) : int =
  bg |> Array.sum (Array.count (fun beams -> List.length beams > 0))
;;

let find_best_start (g : Grid.t) : beams_grid =
  let w, h = Grid.size g in

  let max_len = ref 0 in
  let m_bg = ref (Array.make_matrix 0 0 []) in

  let update_max dir0 pos0 =
    let bg = simulate_beams g ~dir0 ~pos0 in
    let len = count_energized bg in
    if len > !max_len then begin
      max_len := len;
      m_bg := bg
    end
  in

  0 => w - 1 |> Seq.iter (fun x -> update_max Down { x; y = 0 });
  0 => w - 1 |> Seq.iter (fun x -> update_max Up { x; y = h - 1 });
  0 => h - 1 |> Seq.iter (fun y -> update_max Right { x = 0; y });
  0 => h - 1 |> Seq.iter (fun y -> update_max Left { x = w - 1; y });
  !m_bg
;;

let solve_1 data = data |> simulate_beams ~dir0:Right ~pos0:{ x = 0; y = 0 } |> count_energized
let solve_2 data = data |> find_best_start |> count_energized

let () =
  let data = Grid.of_string_list (read_lines stdin []) in
  print_endline (string_of_int (solve_1 data));
  print_endline (string_of_int (solve_2 data))
;;
