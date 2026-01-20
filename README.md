# 🍛 Cury Company — Business Intelligence & Data Analysis

## 📌 Visão Geral
Este projeto tem como objetivo desenvolver um painel estratégico de indicadores (KPIs) para a Cury Company, uma empresa de tecnologia que atua no modelo de negócio Marketplace, conectando restaurantes, entregadores e pessoas compradoras. O painel fornece visibilidade clara e centralizada dos principais indicadores de crescimento da empresa, auxiliando o CEO na tomada de decisões estratégicas.

## 🎯 Problema de Negócio
Apesar do crescimento constante no número de pedidos, a Cury Company não possuía uma ferramenta unificada que permitisse acompanhar o crescimento do volume de pedidos, a performance dos entregadores e a eficiência logística dos restaurantes. Antes da aplicação de modelos de Machine Learning, a empresa precisava estruturar seus KPIs estratégicos em um painel visual, simples e acessível.

## 📊 Métricas do Projeto
Do lado da empresa, foram analisadas métricas como quantidade de pedidos por dia e por semana, distribuição dos pedidos por tipo de tráfego, comparação do volume de pedidos por cidade e tipo de tráfego, quantidade de pedidos por entregador por semana e a localização central de cada cidade por tipo de tráfego. Do lado dos entregadores, foram avaliadas a menor e maior idade, a melhor e a pior condição dos veículos, a avaliação média por entregador, a avaliação média e o desvio padrão por tipo de tráfego e por condições climáticas, além do ranking dos 10 entregadores mais rápidos e mais lentos por cidade. Do lado dos restaurantes, foram analisadas a quantidade de entregadores únicos, a distância média entre restaurantes e locais de entrega, o tempo médio e o desvio padrão de entrega por cidade, por tipo de pedido e por tipo de tráfego, além do tempo médio de entrega durante festivais.

## 🧠 Premissas da Análise
A análise foi realizada com dados entre 11/02/2022 e 06/04/2022, considerando o modelo de negócio Marketplace. As três principais visões adotadas foram: transações de pedidos, restaurantes e entregadores.

## 🛠️ Estratégia da Solução
O painel foi estruturado em três visões estratégicas. A visão de crescimento da empresa contempla pedidos por dia e por semana, pedidos por tipo de entrega e pedidos por cidade e tipo de tráfego. A visão de crescimento dos restaurantes analisa pedidos únicos, distância média percorrida, tempo médio e desvio padrão de entrega, além da comparação entre dias normais e festivais. A visão de crescimento dos entregadores aborda faixa etária, avaliação por veículo, avaliação por tráfego e clima e a performance dos entregadores mais rápidos.

## 💡 Principais Insights
Foi identificada uma sazonalidade diária nos pedidos, com variação média de aproximadamente 10% entre dias consecutivos. Observou-se que cidades classificadas como Semi-Urban não apresentam condições de tráfego baixo. Além disso, as maiores variações no tempo de entrega ocorrem em condições climáticas ensolaradas.

## 🚀 Produto Final
O produto final é um dashboard interativo online, hospedado em Cloud e acessível por qualquer dispositivo conectado à internet. O painel pode ser acessado pelo link: https://currycompany-vitor.streamlit.app/

## 🧪 Tecnologias Utilizadas
O projeto foi desenvolvido utilizando Python, Pandas, NumPy, Plotly e Streamlit.

## ✅ Conclusão
O projeto atingiu seu objetivo ao fornecer uma visão clara e integrada dos KPIs da empresa. A partir da visão da empresa, foi possível identificar um crescimento no número de pedidos entre a semana 06 e a semana 13 do ano de 2022, reforçando a importância do monitoramento contínuo dos indicadores.

## 🔮 Próximos Passos
Como próximos passos, sugere-se a redução do número de métricas exibidas, a criação de novos filtros interativos e a inclusão de novas visões estratégicas do negócio.

## 👩‍💻 Autoria
Projeto desenvolvido como parte de estudos em Data Science e Business Intelligence, com foco em análise estratégica de dados e visualização para tomada de decisão.
