# ML-Hub
Projeto que visa oferecer um hub de analises de ML (Machine Learning) para rápida e fácil submissão de dados e obtenção de insigths, as principais características desta interface serão:

- Fornecer uma factory para Pré processamento de dados brutos
- Fornecer uma factory para instancia de modelos de ML (Isso significa, passar os dados processados e obter como retorno um modelo pronto para inferência, para técnicas/ modelos específicos)

## Objetivos:

- Ser escalável e otimizado
- Poder ser utilizado em quase qualquer conjunto de dados
- Oferer uma interface plug and play

## Como realizar uma implementação? (Mind map)

1. Conecte sua aplicação no websocket do servidor
2. Envie eventos para o servidor com o formato correspondente com o que deseja realizar:

## Tags:

### Processar arquivos csv:
```
{
    "type":"file",
    "func":"from_csv"
    "args":[ARGS]
}
```

### Pré-processar dados:
```
{
    "type":"pre-processing",
    "datasset":[DADOS-EM-JSON],
    "target":[TARGETS],
    "drops":[DROPS]
}
```

### Criar uma instância de um modelo:
```
{
    "type":"create-model"
    "model":[TIPO-DO-MODELO], #Ex: random-forest
    "args":{
        "X_train":[DADOS-PRÉ-PROCESSADOS],
        "y_train":[DADOS-PRÉ-PROCESSADOS],
        "X_test":[DADOS-PRÉ-PROCESSADOS],
        "y_test":[DADOS-PRÉ-PROCESSADOS]
    }
}
```

### Carregar um modelo pré-treinado:
```
{
    "type":"load-model",
    "name":[CAMINHO/PARA/O/ARQUIVO.joblib]
}
```

## Arquivos e concerns:

As principais funções do presente projeto giram em torno dos arquivos ```data.py``` e ```models.py```

### ```data.py```:
Arquivo responsável pelas funções de datasset/dados no geral, desde a modelagem, até o pré processamento dos mesmos, também inclui funções que lidam com arquivos e as importações destes, também responsável pela geração de insigths sobre esses dados, antes do processo de aplicação do modelo

### ```models.py```:
Arquivo responsável pelas funções e instâncias de modelos de ML, encapsula as aplicações destes, desde tarefas de regressão, classificação, NLP e etc... encorpora por si só uma mais facil implementações destes. 