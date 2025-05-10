import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import japanize_matplotlib
    import polars as pl
    return mo, np, pl, plt, sns


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
    g = mo.ui.slider(0, 0.001, value=0.00005, step=0.000001, label="金利の伸び率(年利)")
    r_lim = mo.ui.slider(0.001, 0.1, value=0.04, step=0.001, label="金利上限(年利)")
    T = mo.ui.slider(10, 50, value=35, step=1, label="ローン年数")
    P = mo.ui.slider(3000, 15000, value=8000, step=100, label="借入額")

    mo.vstack([
        mo.md("# パラメーター設定"),
        mo.md(f"**当初金利水準(年利)**: {r_0}"),
        mo.md(f"**金利の伸び率(年利)**: {g}"),
        mo.md(f"**金利上限(年利)**: {r_lim}"),
        mo.md(f"**ローン年数**: {T}年"),
        mo.md(f"**借入額**: {P}万円"),

    ])


    return P, T, g, r_0, r_lim


@app.cell(hide_code=True)
def _(P, T, g, mo, r_0, r_lim):
    # 月次計算のためのパラメータ変換
    r_0_monthly = r_0.value / 12  # 月利に変換
    g_monthly = g.value/12     # 月あたりの伸び率に変換
    r_lim_monthly = r_lim.value/12     # 月あたりの伸び率に変換
    n_months = T.value * 12       # 総月数
    loan_amount = P.value * 10000

    mo.vstack([
        mo.md(f"**当初金利水準(年利)**: {r_0.value*100}％（月利{r_0_monthly * 100:.3f}％）"),
        mo.md(f"**金利の伸び率(年利)**: {g.value*100}％（月利{g_monthly * 100:.3f}％）"),
        mo.md(f"**金利の上限(年利)**: {r_lim.value*100}％（月利{r_lim_monthly * 100:.3f}％）"),
        mo.md(f"**ローン年数**: {T.value}年（{n_months}か月）"),
        mo.md(f"**借入額**: {P.value}万円"),

    ])
    return g_monthly, loan_amount, n_months, r_0_monthly, r_lim_monthly


@app.cell(hide_code=True)
def _(g_monthly, loan_amount, n_months, np, pl, r_0_monthly, r_lim_monthly):

    # 各月の金利率を計算（変動金利のため）
    monthly_rates = np.array([min(r_0_monthly + i * g_monthly, r_lim_monthly) for i in range(n_months)])

    months = np.arange(1, n_months + 1)

    # 元利均等返済の計算
    principal_and_interest_payments = []
    principal_and_interest_balance = []
    principal_and_interest_principal = []
    principal_and_interest_interest = []

    # 元金均等返済の計算
    equal_principal_payments = []
    equal_principal_balance = []
    equal_principal_principal = []
    equal_principal_interest = []

    # 残高の初期化
    pi_balance = loan_amount
    ep_balance = loan_amount

    # 各月の返済額を計算
    for i, month in enumerate(months):
        current_rate = monthly_rates[i]
    
        # 1. 元利均等返済の計算
        # 残りの期間で毎月同じ額を返済する計算（金利上昇を考慮）
        remaining_months = n_months - i
    
        if remaining_months > 0:
            # 将来の平均金利を近似計算
            future_rates = monthly_rates[i:i+remaining_months]
            avg_future_rate = np.mean(future_rates)
        
            # PMT関数と同等の計算
            if avg_future_rate > 0:
                pi_payment = pi_balance * avg_future_rate * (1 + avg_future_rate) ** remaining_months / ((1 + avg_future_rate) ** remaining_months - 1)
            else:
                pi_payment = pi_balance / remaining_months
        else:
            pi_payment = pi_balance
    
        # 利息と元金の分解
        pi_interest = pi_balance * current_rate
        pi_principal = pi_payment - pi_interest
        # 残高更新
        pi_balance -= pi_principal
    
        # 結果を記録
        principal_and_interest_payments.append(pi_payment)
        principal_and_interest_balance.append(pi_balance)
        principal_and_interest_principal.append(pi_principal)
        principal_and_interest_interest.append(pi_interest)
    
        # 2. 元金均等返済の計算
        # 数式: 毎月の返済額 = P/T + P/T * (T - τ) * r_m
        # ただし、τは支払い経過月（1始まり）
        ep_principal = loan_amount / n_months  # 毎月同じ額の元金返済
        ep_interest = ep_balance * current_rate  # 残高に対する利息
        ep_payment = ep_principal + ep_interest  # 毎月の返済額
    
        # 結果を記録
        equal_principal_payments.append(ep_payment)
        equal_principal_principal.append(ep_principal)
        equal_principal_interest.append(ep_interest)

        # 残高更新
        ep_balance -= ep_principal
        equal_principal_balance.append(ep_balance)

    payment_data = []

    # データフレーム用にデータを整形
    for i, month in enumerate(months):
        # 元利均等返済の月々の支払い
        payment_data.append({
            "month": month, 
            "amount": principal_and_interest_payments[i], 
            "type": "元利均等返済（総支払額）"
        })
    
        # 元利均等返済の利息部分
        payment_data.append({
            "month": month, 
            "amount": principal_and_interest_interest[i], 
            "type": "元利均等返済（利息部分）"
        })
    
        # 元利均等返済の元金部分
        payment_data.append({
            "month": month, 
            "amount": principal_and_interest_principal[i], 
            "type": "元利均等返済（元金部分）"
        })
    
        # 元金均等返済の月々の支払い
        payment_data.append({
            "month": month, 
            "amount": equal_principal_payments[i], 
            "type": "元金均等返済（総支払額）"
        })
    
        # 元金均等返済の利息部分
        payment_data.append({
            "month": month, 
            "amount": equal_principal_interest[i], 
            "type": "元金均等返済（利息部分）"
        })
    
        # 元金均等返済の元金部分
        payment_data.append({
            "month": month, 
            "amount": equal_principal_principal[i], 
            "type": "元金均等返済（元金部分）"
        })
    
    # 残高推移のデータ
    balance_data = []
    for i, month in enumerate(months):
        balance_data.append({
            "month": month, 
            "balance": principal_and_interest_balance[i], 
            "type": "元利均等返済"
        })
        balance_data.append({
            "month": month, 
            "balance": equal_principal_balance[i], 
            "type": "元金均等返済"
        })


    payment_df = pl.DataFrame(payment_data)
    balance_df = pl.DataFrame(balance_data)
    return balance_df, payment_df


@app.cell(hide_code=True)
def _(payment_df, pl, plt, sns):
    sns.lineplot(data = payment_df.filter(pl.col('type').str.contains('元金均等')).to_pandas(),
                 x = 'month',
                y = 'amount',
                hue = 'type',
                )
    plt.title("元金均等方式での支出")
    plt.xlabel('経過月数')
    plt.ylabel('支払額（円）')
    plt.show()
    return


@app.cell(hide_code=True)
def _(payment_df, pl, plt, sns):
    sns.lineplot(data = payment_df.filter(pl.col('type').str.contains('元利均等')).to_pandas(),
                 x = 'month',
                y = 'amount',
                hue = 'type',
                )
    plt.title("元利均等方式での支出")
    plt.xlabel('経過月数')
    plt.ylabel('支払額（円）')
    plt.show()
    return


@app.cell(hide_code=True)
def _(balance_df, plt, sns):
    sns.lineplot(data = balance_df.to_pandas(),
                 x = 'month',
                y = 'balance',
                hue = 'type',
                )
    plt.title("方式別残高推移")
    plt.xlabel('経過月数')
    plt.ylabel('残高（円）')
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
