open Utils

type direction = North | South | West | East

(** Move all rocks in the grid towards the given direction until they reach a wall.
    Mutates the given grid. *)
let tilt (dir : direction) (grid : Grid.t) : Grid.t =
  (* The idea is to iterate on linear sequences of indices depending
     on the direction without having to rotate the whole grid repeatedly.
     This counts and removes rocks along the way then when a wall or end
     is found, "n_rocks" previous cells are changed to rocks. *)
  let n_rocks = ref 0 in
  let _rock y x =
    n_rocks := !n_rocks + 1;
    grid.(y).(x) <- '.'
  in
  let _wall ?(dy = 0) ?(dx = 0) y x =
    for i = 1 to !n_rocks do
      grid.(y + (i * dy)).(x + (i * dx)) <- 'O'
    done;
    n_rocks := 0
  in
  let _cell ?(dy = 0) ?(dx = 0) y x =
    match grid.(y).(x) with
    | 'O' -> _rock y x
    | '#' -> _wall ~dy ~dx y x
    | _ -> ()
  in
  let iter size op start f = Seq.init size (op start) |> Seq.iter f in
  let h, w = Grid.size grid in
  let ys, xs = (iter h, iter w) in
  let m = -1 in
  match dir with
  | North -> xs (+) 0 (fun x -> ys (-) (h-1) (fun y -> _cell ~dy:1 y x); _wall ~dy:1 m x); grid
  | South -> xs (+) 0 (fun x -> ys (+) 0     (fun y -> _cell ~dy:m y x); _wall ~dy:m h x); grid
  | West  -> ys (+) 0 (fun y -> xs (-) (w-1) (fun x -> _cell ~dx:1 y x); _wall ~dx:1 y m); grid
  | East  -> ys (+) 0 (fun y -> xs (+) 0     (fun x -> _cell ~dx:m y x); _wall ~dx:m y w); grid
;;

let mem_grid : (string, string * int) Hashtbl.t = Hashtbl.create 100
let mem_cycle : (int, int) Hashtbl.t = Hashtbl.create 100
let tilt_nwse grid = grid |> tilt North |> tilt West |> tilt South |> tilt East

let rec tilt_cycle ?repeat:(n = 1) ?(shorting = false) (grid : Grid.t) : Grid.t =
  if n < 1 then grid
  else if shorting then tilt_cycle ~repeat:(n - 1) ~shorting:true (tilt_nwse grid)
  else
    let grid_id = Grid.to_string grid in
    match Hashtbl.find_opt mem_grid grid_id with
    | Some (saved_grid, saved_n) -> (
        let new_grid = Grid.of_string saved_grid in
        match Hashtbl.find_opt mem_cycle saved_n with
        | Some past_n ->
            let size = past_n - n in
            let dest = (n mod size) - 1 in
            (* Printf.printf "Distinct grids: %d\n" (Hashtbl.length mem_grid); *)
            (* Printf.printf "Cycle detected %d -> %d (size=%d) (dest=%d)\n%!" past_n n size dest; *)
            tilt_cycle ~repeat:dest ~shorting:true new_grid
        | None ->
            Hashtbl.add mem_cycle saved_n n;
            tilt_cycle ~repeat:(n - 1) new_grid)
    | None ->
        let new_grid = tilt_nwse grid in
        (* Printf.printf "New cycle entry n=%d:\n%!" n; *)
        Hashtbl.add mem_grid grid_id (Grid.to_string new_grid, n);
        tilt_cycle ~repeat:(n - 1) new_grid
;;

let row_score h y row =
  let score = (h - y) * (row |> Array.to_seq |> Seq.filter (( = ) 'O') |> Seq.length) in
  (* Row.print row; Printf.printf "  %d\n" score; *)
  score
;;

let grid_score (grid : Grid.t) =
  let h = Array.length grid in
  grid |> Array.mapi (row_score h) |> Array.fold_left ( + ) 0
;;

let solve_1 data = grid_score (tilt North data)
let solve_2 data = grid_score (tilt_cycle ~repeat:1_000_000_000 data)

let () =
  let data = Grid.of_string_list (read_lines stdin []) in
  (* Grid.print data; *)
  print_endline (string_of_int (solve_1 data));
  print_endline (string_of_int (solve_2 data))
;;
