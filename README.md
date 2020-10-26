# Neuroteks PDF Manipulation API

[@author.github](https://github.com/Onmaedi/)

[@author.mail](mailto:http://gmail.com/)

### ntks-pdf-manipulation-api

# Instalação

> Dependências

- Python 3.x
- pip

1. Instanlando o pipenv

```bash
python3 -m pip install pipenv
```

2. Clone o repositório.

```bash
git clone https://github.com/Onmaedi/ntks-pdf-manipulation-api.git
```

3. Dentro do diretório execute:

```bash
pipenv install
```

4. Crie um arquivo `.env`

```
FLASK_ENV=development
FLASK_APP=src.app:create_app
DROPBOX_TOKEN=<your-dropbox-api-token>
```

# Rodando o projeto

Dentro da sua virtual env do python pode somente executar o comando:

```bash
flask run
```

ou (não recomendado):

```bash
python main.py
```

# Rotas

## PDF-MERGE-FOLDER

```
api.mergedropboxfolder  POST     /api/v1/pdf-merge-folder
```

Para realizar o merge de todos os arquivos dentro de uma pasta do Dropbox.
A pasta que será realizada o merge será passada via parâmetro no `json` da requisição.
Iniciando sempre com uma `/` antes do nome da pasta.

```json
{
  "folderPath": "/pastaDesejada"
}
```

Se houver subpastas elas deverão ser separadas também com uma `/` para cada nível de pasta.

```json
{
  "folderPath": "/pastaDesejada/subPastaDesejada"
}
```

A resposta será um json com o base64 do pdf unificado e com um array dizendo quais os arquivos foram juntados.

```json
{
  "filesMerged": [...],
  "base64file": "..."
}
```

---

## PDF-MERGE-DROPBOX

```
api.pdfmergerdropbox    POST     /api/v1/pdf-merge-dropbox
```

Para realizar o merge de arquivos especificos dentro do Dropbox precisa passar o caminho de todos os arquivos iniciando com `/` passando o caminho até o caminho do(s) arquivo(s) desejado(s).

```json
{
  "files": ["/neuroteks/d1.pdf", "/neuroteks/d2.pdf"]
}
```

A resposta será um json com o base64 do arquivo unificado.

```json
{
  "base64file": "..."
}
```

---

## PDF-MERGE

Para realizar o merge de arquivos especificos e que não estão diretamente no Dropbox.
O merge desses arquivos serão feitos de um base64 enviado para a api.

```
api.pdfmerger           POST     /api/v1/pdf-merge
```

```json
{
  "files": ["...", "..."]
}
```

A resposta será um json com o base64 do arquivo unificado.

```json
{
  "base64file": "..."
}
```

---

## PDF-WRITE

```
api.pdfwriter           POST     /api/v1/pdf-write
```

Para escrever uma ou mais `string` em um arquivo pdf desejado, precisa ser enviado o base64 do arquivo e as `strings` desejadas.
As strings estarão presentes em todas as páginas do arquivo sendo escritas no canto superior direito.

```json
{
  "content_text": ["Neuroteks", "01-01-2020", "123"],
  "file": "..."
}
```

A resposta será um json com o base64 do arquivo gerado.
