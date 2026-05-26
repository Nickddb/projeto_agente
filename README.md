# AI AGENT de Nicolle Rocha
![Gemini](https://img.shields.io/badge/Gemini-7A9BEE.svg?style=for-the-badge&logo=googlegemini&logoColor=white)
![AI Robot](https://img.shields.io/badge/%F0%9F%A4%96-Artificial%20Intelligence-4AE8DE.svg?style=for-the-badge)

## **Sobre**
Este projeto foi feito para testar e ampliar minhas capacidades de lidar com a tecnologia, que muda constantemente. Diferentes aplicações foram utilizadas, a fim de poder ter resultados mais precisos e completos, ajudando na formação de percepção do usuário sobre assuntos específicos. Por enquanto, há um orquestrador que irá checar os agentes que abordarãos os temas de **zoologia**, **matemática** e **filmes** (utilizando uma API própria do TMDB).

<br>
<br>

## **Contextualização**

### **LLM**
Tudo começa com a Language Learning Model, também conhecida como Generative Pre-Trained Transformer, o primeiro passo para o que virá a se tornar um robô autônomo. Baseado em funções matemáticas e muitas contas de probabilidades, a LLM funciona como a base de um chatbot para escolher quais palavras usar em determinados contextos.

<br>

Exemplos de frases são inseridas em seus bancos de dados e, com a porcentagem de chance de qual será a próxima palavra, o robô consegue criar uma frase, que só saberá que fará sentido ou não se tiver uma avaliação do resultado. Ele pode aprender comparando qual a porcentagem da palavra que estava pensando vs a palavra real da frase, por exemplo.

<br>

Para realizar tantas contas e tentativas, são necessários chips de computadores especiais feitos para rodarem várias aplicações simultaneamente, conhecidos por **GPUs**.
O processo envolve o raciocínio e análise dos resultados, em que o agente *dinamicamente* decide como irá realizar a tarefa, revisa seus passos, aciona tools e determina quando irá parar. Mas no final, haverá uma pessoa atuando como mediador desse agente, que dará decisões, demandas e observações de resultados.
***

<br>
<br>

## **Outros conceitos** 
* **Transformer:** um sistema criado por pesquisadores da Google, que analiza várias palavras ao mesmo tempo. Contém o Feedfoward, um sistema de capacidade que abriga os padrões reconhecidos pela IA durante o treinamento, que relaciona palavras com números;

<br>

* **Workflow agents**, diferentemente de AI agents, precisa totalmente de um controle humano para guiar as etapas e lógica. Também funciona com base no LLM e completa tarefas bem-definidas, garantindo uma atuação mais consistente e previsível. 
É ideal para atividades repetitivas e padronizadas, mas pode ser inserido num contexto de AI agent;

<br>

* **ADK** VS **SDK**

    <br>

    ADK, **Agent Development Kit**, é focado na criação de agentes autônomos e workflows que diagnostiquem anomalias, leiam logs, e tomem decisões baseadas em objetivos.

    <br>
    
    SDK, **Software Development Kit**, é a base de tools usada para criar apps para uma determinada plataforma, importar APIs, hospedar um serviço na nuvem, etc. O desenvolvedor tem controle total sobre as lógicas e etapas.
***

<br>
<br>

## A lógica

### ORQUESTRADOR
O sistema funciona com base em um único orquestrador, que, assim que receber o prompt, irá analizar se consegue responder por conta própria. Caso negativo, irá buscar em seus agentes a resposta, podendo utilizar de funções e chaves APIs para consultar seus bancos de dados.

A função que o descreve importa o Gemini 2.5 Flash, que tem maior cota diária de tokens, e lembra o histórico da conversa. 
