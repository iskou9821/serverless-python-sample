# 概要
Serverless Frameworkで、FlaskのアプリケーションをAWS上にデプロイするサンプルです。

# 実行方法
## 事前準備
Serverless Frameworkは、node.jsで動作します。

そのため、まずnode.jsをインストールし、npmコマンドが利用できる状態にしておいて下さい(説明は割愛します)。

なお、pythonのバージョンは3.6であるものと想定しています。

また、これ以降の作業はすべて、serverless.ymlの存在するディレクトリで実行するものとします。


## Serverless Frameworkのインストール
```
npm install -g serverless
```

を実行します。

それにより

```
sls
```

コマンドで、serverless frameworkが動作するようになります。

## IAMユーザーを作成
AWS Console上から、デプロイを実行するためのユーザーを作成します(こちらも、詳細な手順は割愛します)。

とりあえずテスト用であれば、一時的にAdministratorAcceessを与えてしまうのが一番簡単です。

私もまだ正確には把握していませんが

 * S3
 * API Gateway
 * AWS Lambda
 * Cloudformation
 * IAM

に対して読み込み/書き込み権限を持っていれば、大体動くかと思います。

 * Serverless Frameworkは、S3やLambdaやAPI Gatewayなど、色々なところに自動でリソースを作りまくるので、**本番で利用しているアカウントでいきなりデプロイするのは、あまりお勧めしません。**
 * Lambda functionが利用するIAM Roleや、アップロード先となるS3 bucketなど、デプロイの際に利用するリソースを自動生成させず、予め指定するようにすることでも、必要な権限を減らすことができます。

## ~/.aws/credentialsの編集
ユーザーを作成したら、上記ファイルにアクセスキーを書いておきます。

```
[test]
aws_access_key_id = [key-id]
aws_secret_access_key = [secret-access-key]
```

[test]の部分は、適当に設定してしまってOKです。

## serverless.ymlの編集
serverless.ymlの「provider」→「profile」の部分を、先ほど~/.aws/credentialsに記載したプロファイル名に書き換えておきます。

## プラグインのインストール
```
npm install
```
を実行し、serverless-wsgiプラグインをインストールします。

## アプリケーションをローカルで起動する場合
virtualenvを作成するなどして、requirements.txtに記載されたモジュールをインストールした後

```
sls wsgi serve
```

を実行すると、localhostでアプリケーションが起動されます。

なお、requirements.txtからのモジュールのインストールは

```
pip install -r requirements.txt
```

で可能です。

http://localhost:5000/helloにアクセスし

```
{
  "message": "hello, world!", 
  "success": true
}
```
のように表示されればOKです。

＊pycharmなどのIDEから直接起動したい場合は、「app_run.py」を実行すればOKです。

## アプリケーションをデプロイする
```
sls deploy
```

を実行すると、AWS上にアプリケーションがデプロイされます。

デプロイが完了すると、

＊ **virtualenvなどで環境切り替えが行われているとデプロイに失敗します** ので、virtualenvが有効となっている場合には、deactivateするなどして、元に戻しておいてください。

コマンドを実行した後

```
Service Information
service: serverless-test
stage: dev
region: ap-northeast-1
api keys:
  None
endpoints:
  ANY - https://[固有の番号]-api.ap-northeast-1.amazonaws.com/dev/{proxy+}
functions:
  api: serverless-test-dev-api

```

のように表示されれば成功です。

https://[固有の番号].execute-api.ap-northeast-1.amazonaws.com/dev/hello

にアクセスすると、ローカル実行した場合と同じメッセージが表示されると思います。

## 確認
sls deployを実行すると、以下のようなリソースが作成されます。

 * AWS Lambda関数
 * API GatewayのAPI、及びリリース
 * AWS LambdaにデプロイするためのS3バケット
 * API Gatewayを作成するためのCloudFormationスタック
 * AWS Lambdaを実行するためのIAM Role

管理コンソールから、リソースが追加されていることをご確認ください。
