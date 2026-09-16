# Lagrange kalanındaki ksi'nin somutlanması

Lagrange kalanı bir eşitliktir:

```
f(x) = P_N(x) + f^(N+1)(ksi)/(N+1)! * (x-a)^(N+1)
```

Aşağıdaki ksi değerleri **arandı ve bulundu**; son sütun eşitliğin iki yanı arasındaki farktır (kayan nokta gürültüsü mertebesinde).

| fonksiyon | N | x    | bulunan ksi   | (a,x) içinde mi? | eşitlik artığı |
|-----------|---|------|---------------|------------------|----------------|
| sin(x)    | 3 | 1.2  | 0.2340652903  | evet             | 0.00e+00       |
| sin(x)    | 6 | 2.5  | 0.4079533252  | evet             | 0.00e+00       |
| exp(x)    | 4 | 1    | 0.1771577599  | evet             | 0.00e+00       |
| exp(x)    | 4 | -1.5 | -0.2294380888 | evet             | 0.00e+00       |
| ln(1+x)   | 5 | 0.7  | 0.0809115208  | evet             | 0.00e+00       |
| 1/(1-x)   | 3 | 0.5  | 0.1294494367  | evet             | 0.00e+00       |
| ln(1+x)   | 6 | 1.8  | 0.1435686869  | evet             | 4.22e-15       |

Son satır özellikle önemli: `ln(1+x)`, `x=1.8` noktası yakınsaklık yarıçapının (R=1) **dışındadır**. Seri orada ıraksar, yani N→∞ limitinde P_N(1.8) hiçbir yere gitmez. Buna rağmen sonlu N için eşitlik hâlâ geçerlidir ve ksi hâlâ vardır. **Taylor polinomu ile Taylor serisi aynı şey değildir.**
