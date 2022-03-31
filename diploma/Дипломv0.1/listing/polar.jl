include("src/RK.jl")
include("src/parameters.jl")

# Если аргументы не переданы или переданы некорректно, то рисуем линзу Люнеберга
if (length(ARGS) > 0 && ARGS[1] == "maxwell")
  lens = "maxwell"
  include("src/maxwell.jl")
else 
  lens = "luneburg"
  include("src/luneburg.jl")
end

include("src/polar_eikonal.jl")

# Создаем директорию, куда будем сохранять результаты расчетов
isdir(dir[lens]) ? true : mkdir(dir[lens])

# x_0, y_0, p1_0, p2_0
xn_0 = Vector{Float64}(undef, 4)

# Источник точечный. Из него под углом α расходятся лучи
for (i, α) in enumerate(range(α_min, stop=α_max, length=30))
  # Лучи исходят из одной точки, расходясь под углом α к оси Ох
  xn_0[1:2] = [r_0, phi_0]
  xn_0[3:4] = [-cos(α)*n(r_0), -sin(α)*n(r_0)]

  tn, xn = RK.RKp6n1(eikonal, xn_0, h, t_start, t_stop)

  file = open("./$(dir[lens])/data$i.txt", "w")
  for (t, x, y) in zip(tn, xn[:, 1], xn[:, 2])
    write(file, "$t,$x,$y\n")
  end
  close(file)
  
  # для отображения прогресса
  print("=")
end
println()
