import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib as plt
    import seaborn as sns

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # 住宅ローンシミュレーション
    ここでは、住宅ローンについての返済パターンを概観した後、総返済額及び月毎の支払額についてみる。なお、各種補助金・税額控除については現時点では扱わないこととする。

    ## ローンの種類
    - 金利
        - 固定
            - 金利が固定されている。現在は割高であるものの、将来的に大きく伸びることを見越すならこちら
        - 変動
            - インフレがどんどん加速しない場合はこちら
    - 月々の支払い
        - 元利均等
            - 月々の支払いが安定するものの、総支払額は高くなる
        - 元金均等
            - 総支払額は安くなるものの、前半の持ち出しが高くなる
    ## 変動金利の式
    いずれの場合においても、固定金利の場合は$r_m$は定数。変動金利の場合は可変パラメーター。

    - 元利均等返済

        $$毎月の返済額 = \frac{r_m * (1+r_m)^T}{(1+r_m)^T -1} * P$$
    ただし、$r_m$は月利、$T$は総返済回数、$P$は借入額

    - 元金均等返済

        $$毎月の返済額 = \frac{P}{T} + \frac{P}{T}*(T-\tau)*r_m$$
    ただし、$r_m$は月利、$T$は総返済回数、$\tau$は支払い経過月、$P$は借入額


    ## ソース
    - [住宅ローン金利の計算方法をシミュレーションと共にご紹介](https://www.smbc.co.jp/kojin/jutaku_loan/column/kinri_calculation/)
    - [住宅ローン計算も分かる利息計算，債務返済方法の算式](https://www5d.biglobe.ne.jp/Jusl/Kasikin/RisokuKeisan.html)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    r_0 = mo.ui.slider(0.001, 0.1, value=0.02, step=0.001, label="当初金利水準(年利)")
    g = mo.ui.slider(0, 0.1, value=0.001, step=0.001, label="金利の伸び率(年利)")
    T = mo.ui.slider(10, 50, value=35, step=1, label="ローン年数")
    P = mo.ui.slider(3000, 15000, value=8000, step=100, label="借入額")

    mo.vstack([
        mo.md("# パラメーター設定"),
        mo.md(f"**当初金利水準(年利)**: {r_0}"),
        mo.md(f"**金利の伸び率(年利)**: {g}"),
        mo.md(f"**ローン年数**: {T}年"),
        mo.md(f"**借入額**: {P}万円"),

    ])
    return P, T, g, r_0


@app.cell(hide_code=True)
def _(P, T, g, mo, r_0):
    mo.vstack([
        mo.md(f"**当初金利水準(年利)**: {r_0.value*100}％（月利{r_0.value*100/12:.3f}％）"),
        mo.md(f"**金利の伸び率(年利)**: {g.value*100}％（月利{g.value*100/12:.3f}％）"),
        mo.md(f"**ローン年数**: {T.value}年（{T.value * 12}か月）"),
        mo.md(f"**借入額**: {P.value}万円"),

    ])
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
