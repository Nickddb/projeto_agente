# AI AGENT de Nicolle Rocha
![Gemini](https://img.shields.io/badge/Gemini-7A9BEE.svg?style=for-the-badge&logo=googlegemini&logoColor=white)
![AI Robot](https://img.shields.io/badge/%F0%9F%A4%96-Artificial%20Intelligence-4AE8DE.svg?style=for-the-badge)

## **Sobre**
Este projeto foi feito para testar e ampliar minhas capacidades de lidar com a tecnologia, que muda constantemente. Diferentes aplicações foram utilizadas, a fim de poder ter resultados mais precisos e completos, ajudando na formação de percepção do usuário sobre assuntos específicos. Por enquanto, há um orquestrador que irá checar os agentes que abordarãos os temas de **biologia**, **matemática** e **filmes** (utilizando uma API própria do TMDB).

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

    ADK, **Agent Development Kit**, é focado na criação de agentes autônomos e workflows que diagnostiquem anomalias, leiam logs, e tomem decisões baseadas em objetivos.

    SDK, **Software Development Kit**, é a base de tools usada para criar apps para uma determinada plataforma, importar APIs, hospedar um serviço na nuvem, etc. O desenvolvedor tem controle total sobre as lógicas e etapas.
***

<br>
<br>

## A lógica
O código começa com uma série de instruções que serão passadas para os agentes e orquestrador, que deverão responder a pergunta do usuário de acordo com suas especialidades. Se a pergunta for fora de seu escopo, o sistema evitará respondê-la.

<br>

### ORQUESTRADOR
O sistema funciona com base em um único orquestrador, que, assim que receber o prompt, irá analizar se consegue responder por conta própria. Caso negativo, irá buscar em seus agentes a resposta, podendo utilizar de funções e chaves APIs para consultar seus bancos de dados. Ao ser questionado, o código descobre qual tool o Gemini quer usar e extrai os argumentos que ele sugeriu e executa a função

<br>

A função que o descreve importa o Gemini 2.5 Flash, que tem maior cota diária de tokens, e lembra o histórico da conversa. Ele é um modelo rápido e econômico (nos quesitos financeiros, de limites da API (mais requisições por minuto - RPM - e mais tokens por minuto - TPM), tempo (de resposta)) e tem como customizar seu índice de foco, neste caso sendo de 0.3, para que ele evite gerar respostas desconexas do assunto. Há um contador que serve como pausa de segurança para não estourar o limite de requisições por minuto do plano gratuito e é acionado um tratamento amigável para o erro de cota se o usuário digitar rápido demais.
***

### CALCULADORA
Esta função depende de funções específicas da biblioteca Math, que irá auxiliar a calcular contas complexas e a filtrar números e operações no comando que o usuário for inserir.

<br>

Um exemplo dessas funções é o **Dict**, que ignora tudo que começa com ****__**** (config. interna do python);

**Variáveis** incluem funções absolutas do Python (função nativa (built-in) abs()) que são úteis em matemática;

**Eval** = a string é executada como código python puro. Isso significa poder considerar apenas as equações presentes;

**builtins**: torna indisponíveis as funções padrões do python;

**allowed_names**: torna disponíveis apenas as funções permitidas que foram filtradas do Math;
Por fim, se algo for digitado errado, retornará uma mensagem de erro.
***

<br>

### FILMES - TMDB
Este agente irá se conectar à API do TMDB para conseguir informações específicas do título do filme que for inserido, mas primeiramente foi preciso criar uma conta no site para ter acesso à chave. Seu código inicia lendo o token que foi retirado do site oficial do TMDB, que se não for compreendido corretamente, irá retornar uma mensagem de erro.

Por motivos de segurança, o token é escondido dentro do header, e não exposto diretamente no link URL. URL esta que dependenderá da função **urllib**, que codificará o título do filme e irá até o server TMDB, que, se estiver fora do ar por 10 segundos, o código desiste e imprimirá um aviso de erro.

<br>

Ocorrerá uma verificação para ver se a busca deu certo (Status 200), então focará no primeiro resultado e serão extraídas as suas informações.
***

<br>

Resultados alternativos podem incluir uma mensagem avisando a falta de tradução para português e, num contexto geral, a queda do sistema do Gemini por haver muitas requisições, que impossibilitará de responder a pergunta do usuário.
***

<br>
<br>

### BIOLOGIA
Enquanto os outros agentes possuem códigos próprios que ditam suas ações, o orquestrador não depende de uma função que trate sobre biologia, por ele não depender de funções ou chaves API para trazer à tona dados científicamente corretos, tendo em conta que não é costume esses dados mudarem, nem serem difíceis de encontrar (e precisar de uma API para buscá-los, por exemplo).
Ainda assim, se alguém pedir informações sobre algum tema da biologia, o chatbot irá retornar um texto completo sobre o tema.

<br>

Planejo melhorar este aspecto do código assim que possível, conectá-lo a alguma API que trate sobre riscos de extinção, por exemplo, ou algo mais específico que traga alguma informação legal. 
***

<br>
<br>

## **Como acessar**
Primeiramente, este sistema está rodando a base de **Python**, então para acessá-lo, você terá que ter alguma extensão python baixada previamente.
***

<br>


Entrar na **pasta meu_agente**

cd projeto_agente/meu_agente
***
<br>

**Criar** e **ativar** ambiente virtual

**Windows:**

python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1

<br>

**Mac/Linux:**

python3 -m venv .venv

source .venv/bin/activate
***
<br>

Instalar as **dependências**:

pip install -r requirements.txt
***

<br>

criar um **arquivo .env** dentro da **pasta orquestrador** e preenchê-lo com

GEMINI_API_KEY=sua_chave_do_gemini_aqui
TMDB_API_TOKEN=seu_token_jwt_do_tmdb_aqui

Criar uma conta no TMDB para ter acesso à sua chave.

Ver no Google se você tem permissão para criar sua própria chave também.
***

<br>

Rodar o projeto:

cd orquestrador

python orquestrador.py