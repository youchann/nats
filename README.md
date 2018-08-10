# nats（natsugash）
> myjlab夏合宿チーム用レポジトリ

## 開発環境の構築
Homebrewインストール前提なので、してない人は先にインストールしてね。  
この記事参考に→ [Homebrewインストール手順](https://qiita.com/rabbit1013/items/1494cf345ff172c3b9cd)

### install packages  
仮想環境とpythonのバージョン管理できる他のパッケージ（例えばvirtualenvとか）が既にあるならそっちで仮想環境作っても良いです、多分。  
**インストールするもの**
- pyenv
- pyenv-virtualenv  

この辺参考に。。  
- [pyenvとvirtualenvを使用してPythonの開発環境を構築する](https://uxmilk.jp/43185)
- [pythonの環境構築【pyenvとpyenv-virtualenv】](https://qiita.com/SonoT/items/091d2748deb16fb03653)
- [pyenv, pyenv-virtualenv開発環境の備忘録](https://qiita.com/komi9977/items/697bfa8934e878509d13)
  - `path通すの忘れがち`

**インストールできたら**  
```bash
# 今回は 3.6.5 で作りたいので
$ pyenv install 3.6.5
$ pyenv rehash

# 仮想環境構築
$ cd ~/<各々の作業dir>/nats
$ pyenv virtualenv 3.6.5 natsenv-3.6.5
Requirement already satisfied: setuptools in /Users/iry/.pyenv/versions/3.6.5/envs/natsenv-3.6.5/lib/python3.6/site-packages
Requirement already satisfied: pip in /Users/iry/.pyenv/versions/3.6.5/envs/natsenv-3.6.5/lib/python3.6/site-packages

# natsディレクトリにnatsenv-3.6.5を適用する
# 現在地確認（一応）
$ pwd
/Users/iry/projects/nats
$ pyenv local natsenv-3.6.5

# 確認
$ pyenv versions           
  system
  3.6.3
  3.6.5
  3.6.5/envs/natsenv-3.6.5
* natsenv-3.6.5 (set by /Users/iry/projects/nats/.python-version)
```
**仮想環境のactivate**
```bash
$ pwd
/Users/iry/projects/nats
$ pyenv activate natsenv-3.6.5

# activate後、([env名]) がくっついてれば成功！
(natsenv-3.6.5) [user@host ~]$
```

### requirements.txtについて  
pip経由でパッケージとか追加した時は`pip freeze `で追加したパッケージ見て、requirements.txtに追記する。
- 例（Flaskをインストールしたとき）

```bash
(natsenv-3.6.5)$ pip install Flask
...
(natsenv-3.6.5)$ pip freeze
click==6.7
Flask==1.0.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
Werkzeug==0.14.1
(natsenv-3.6.5)$　
```

natsenv-3.6.5をactivateしている状態で`pip install -r requirements.txt`やると、global汚さずにプロジェクトで必要なパッケージを一括インストールできます。
