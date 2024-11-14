// poller.js

class EndpointPoller {
    constructor(apiKey, baseUrl = 'https://xpt548ceab.execute-api.us-east-1.amazonaws.com/dev') {
        if (!apiKey) {
            throw new Error('API key is required');
        }
        this.api_key = apiKey;
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json',
            'x-api-key': this.api_key
        };
    }

    async run(query, topic, debateType, side, typeOfArgument, render = false) {
        const response = await this.startProcess(query, topic, debateType, side, typeOfArgument);
        this.executionArn = JSON.parse(response.body).executionArn;

        const finalResult = await this.getStatus(this.executionArn);
        const parsedResult = JSON.parse(JSON.parse(finalResult.output).body);

        if (render && parsedResult.html_output) {
            this.renderOutput(parsedResult.html_output);
        }

        return parsedResult;
    }

    async startProcess(query, topic, debateType, side, typeOfArgument) {
        const endpoint = `${this.baseUrl}/polling-serverless-dev-startProcess`;
        const payload = {
            topic,
            debate_type: debateType,
            side,
            query,
            type_of_argument: typeOfArgument
        };

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async getStatus(executionArn, maxAttempts = 30, delay = 10) {
        const endpoint = `${this.baseUrl}/polling-serverless-dev-getStatus`;
        const payload = { executionArn };

        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'SUCCEEDED') {
                return data;
            }

            if (data.status === 'FAILED') {
                throw new Error('Process failed');
            }

            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }

        throw new Error(`Process did not complete after ${maxAttempts * delay} seconds`);
    }

    renderOutput(htmlContent) {
        const container = document.createElement('div');
        container.innerHTML = htmlContent;
        document.body.appendChild(container);
    }
}