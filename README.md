# 分子細胞生物学実験 – ミドリゾウリムシ体内にいるシアノバクテリアの個体数を面積で推定するコード –
# 使い方 
## 前提
- Pythonのインストールはご自分で, Macならデフォルトで入ってるはず, バージョンが古いかもだけど
- このレポジトリを clone
- Python仮想環境がある (PCのglobal環境に直接パッケージとかインストールしてもいいなら必要ない)
  - 仮想環境の構築方法は[こちら](https://qiita.com/shun_sakamoto/items/7944d0ac4d30edf91fde)から
  - 記事に載ってるrequirements.txtに関しては以下で説明

## 必要なパッケージをインストール
1. rootディレクトリで`source bin/activate`して仮想環境を開始 (停止する時はrootディレクトリで`deactivate`)
2. `pip3 install -r requirements.txt`でパッケージたちをインストール

## ゾウリムシの数を蛍光顕微鏡画像の面積で推定することの妥当性を検証する
1. `cd codes`で移動
2. `python3 validity_test.py`
3. `output_images`のrootディレクトリにこんな感じの画像が5枚出てくる
![plausibility_test](https://github.com/user-attachments/assets/d93e9539-44d2-4d2c-83c0-d2ae7336ff87)
4. 以下，プログラムの説明
> [!NOTE]
> 方法の妥当性の検証：シアノバクテリアの個体数と画像の赤の面積に正の相関があることを示す．
> - シアノバクテリアの個体が目視で識別できる画像をまとめる（結果`cyanos`にある16枚が集まった）
> - それぞれの画像で100x100 pixelの範囲を5つ，ゾウリムシが存在する範囲に定める
> - それら100x100 pixel範囲において，目視でシアノバクテリアの個体数をカウントして記録する①
> - 次にプログラムを作成する
>   - 同じ16枚の画像それぞれで，10x10 pixelの範囲をランダムに1万箇所とる（黒だけのところは省く）
>   - その範囲でRGBのRをグレースケールにする
>   - グレースケールにしたRで特定の範囲内の濃さのデータを抽出する
>   - 抽出したデータからそれぞれの画像においての平均値を取る
> - ①を横軸に対応する画像の平均値 ②を縦軸にプロットし，それらの相関関係をみる
> - 有意な正の相関がある場合，赤の面積がシアノバクテリアの個体数を表すのに妥当な指標だと考え，特に相関が強い赤の濃度の範囲を次の画像解析で利用する

> [!CAUTION]
> - この方法の短所は，（消化されたと思われる）輪郭がはっきりしないシアノバクテリアの残骸？も個体としてカウントしていることになる
> - 「赤」でも濃さについて
>   - 赤の濃さは画像をグレースケールにした時に真っ黒（0）〜真っ白（255）の256段階がそれに対応している
>   - 赤をグレースケールにした場合，白い方で赤が強く，黒い方で赤が弱い
>     - `grey_scale.py`を実行すると`input_images/red_grey_scale`にある画像がグレースケールでどの値 (0~255) に当てはまるのかがコマンドラインに出力される
>     -  グレースケールと赤の濃度の関係性がわかる
>   - その256段階を4分割して赤濃度1（0〜50），赤濃度2（51〜101），赤濃度3（102〜152），赤濃度4（153~203），赤濃度5（204〜205）とする
>   - それぞれの赤濃度に対して上記の検証を行い，①との相関が強い（R二乗値が高かったもの）結果に使用した赤の範囲を以後の解析で使用する「赤」とする

## 実際に全ての株のデータでそれぞれのシアノバクテリア濃度について，面積の平均を計算する
1. `python3 analysis.py`
2. `output_images`の`all_analysis_data`に明暗条件においての株ごとにシアノバクテリアそれぞれの濃度勾配において，面積がプロットされてる画像が出てくる
3. 以下，プログラムの説明
> [!NOTE]
> - それぞれの画像の全体においてランダムに10x10 pixelの正方形をとる
> - その正方形内に赤のピクセルがある場合はそれをデータ対象として採択する（もし正方形内のピクセルに赤がない場合，データの対象外とする．）
> - 対象になるデータが1万個になるまで，画像全体でランダムにサンプリングを行う
> - 画像1枚についいて1万個の正方形の赤濃度の平均値を出す．（同じ濃度に複数枚の画像があればそれらの平均値とする．）
> - その平均値がそのゾウリムシ株において，そのシアノバクテリア濃度の結果（ゾウリムシ体内のシアノバクテリアの量的な指標）とする
> - 各ゾウリムシ株においてシアのバクテリアの濃度を横軸，縦軸に赤面積（シアノバクテリア個体数の指標）をおいてプロットする

# 作成者
[@yuyu_lab_tmu](https://x.com/yuyu_lab_tmu) aka 木須 雄士郎

