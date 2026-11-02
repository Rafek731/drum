If[! ValueQ[A], A = 1.];
If[! ValueQ[meshNum], meshNum = 15];
If[! ValueQ[totalFrames], totalFrames = 30];
If[! ValueQ[framesPerSecond], framesPerSecond = 15];

saveDir = FileNameJoin[{Directory[], "Pictures"}];

(* cache BJ0 and omega for faster computation *)

BJ0[m_, n_] := BJ0[m, n] = N@BesselJZero[m, n];

\[Omega][m_, n_] := \[Omega][m, n] = BJ0[m, n];

getFrame[m_, n_, t_] := Module[{x, y},
   Plot3D[
        A BesselJ[m, Sqrt[x^2 + y^2] BJ0[m, n]] Re[((x + I y)/Sqrt[x^2 + y^2])^m] Sin[\[Omega][m, n] t],
        {x, y} \[Element] Disk[{0, 0}, 1],
        PlotRange -> {{-1, 1}, {-1, 1}, {-1.1, 1.1}},
        SphericalRegion -> True,
        Mesh -> meshNum,
        BoxRatios -> {1, 1, 0.4}
    ]
];

makeGif[m_, n_] := Module[{T, dT, frames, path},
    T = N[(2 \[Pi])/\[Omega][m, n]];
    dT = N[T/totalFrames];
    frames = ParallelTable[
        getFrame[m, n, t],
        {t, 0, T - dT, dT}
    ];
    path = FileNameJoin[{saveDir, StringTemplate["membrane_`1`_`2`.gif"][m, n]}];
    Export[
        path,
        frames,
        "AnimationRepetitions" -> Infinity,
        "DisplayDurations" -> 1/framesPerSecond
    ];
    path
];

If[Length[ParallelKernels[]] == 0, LaunchKernels[]];
DistributeDefinitions[A, BJ0];
