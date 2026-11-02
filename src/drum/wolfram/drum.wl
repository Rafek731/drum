(* Vibration modes of a circular membrane fixed at its edge.

   radius R = 1, wave speed c = 1. Mode (m, n) has the shape
     u(r, \[Phi], t) = A J_m(k r) cos(m \[Phi]) sin(\[Omega] t),
   where k is the n-th zero of J_m and \[Omega] = k.

   Loading this file launches the parallel subkernels and sends them
   the definitions; call makeGif afterwards. *)

Options[makeGif] = {"Amplitude" -> 1., "Mesh" -> 15, "Frames" -> 30, "FPS" -> 15};

(* cache BJ0 for faster computation *)
BJ0[m_, n_] := BJ0[m, n] = N@BesselJZero[m, n];

(* c/R should be here but for us it = 1 so skip *)
\[Omega][m_, n_] := BJ0[m, n];

radial[m_, n_, x_, y_] := BesselJ[m, Sqrt[x^2 + y^2] BJ0[m, n]];
angular[m_, n_, x_, y_] := Re[((x + I y)/Sqrt[x^2+y^2])^m]; (* fixes the white stripe *)
time[m_, n_, t_] := Sin[\[Omega][m, n] t];

getFrame[m_, n_, t_, a_, mesh_] := Module[{x, y},
   Plot3D[
        a radial[m, n, x, y] angular[m, n, x, y] time[m, n, t],
        {x, y} \[Element] Disk[{0, 0}, 1],
        PlotRange -> {{-1, 1}, {-1, 1}, {-1.1, 1.1}},
        SphericalRegion -> True,
        Mesh -> mesh,
        BoxRatios -> {1, 1, 0.4}
    ]
];

makeGif[m_, n_, path_, OptionsPattern[]] := Module[{a, mesh, nf, T, dT, frames},
    a = OptionValue["Amplitude"];
    mesh = OptionValue["Mesh"];
    nf = OptionValue["Frames"];
    T = N[(2 \[Pi])/\[Omega][m, n]];
    dT = T/nf;
    frames = ParallelTable[getFrame[m, n, i dT, a, mesh], {i, 0, nf - 1}];
    Export[path, frames,
        "AnimationRepetitions" -> Infinity,
        "DisplayDurations" -> 1/OptionValue["FPS"]]
];

If[Length[ParallelKernels[]] == 0, LaunchKernels[]];
DistributeDefinitions[BJ0, \[Omega], radial, angular, time, getFrame];
