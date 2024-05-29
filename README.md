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
2. Importe seus dados no formato json
3. Envie um evento para o servidor com a tag de ```modeling``` para criar uma instancia de seus dados pré processados ou ```create-model-[MODEL]``` para criar uma instancia de um modelo de ML, substitula ```[MODEL]``` pelo nome do modelo, ex: ```create-model-decisionTree```

**Importante**: Caso vá instanciar o modelo, é importante que seus dados já estejam pré processados e que respeitem os inputs que o modelo em si exige, você pode obter tanto com a função de ```modeling```, quanto você mesmo pode pré processa-los

4. Caso precise que o modelo possa ser usado em novas inferências sem ficar re-treindo-o, você poderá usar a tag ```save-model``` para exportar o modelo treinado. 