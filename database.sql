CREATE TABLE stocks(
    symbol VARCHAR(25),
    country VARCHAR(200),
    industry VARCHAR(200),
    sector VARCHAR(200),
    fullTimeEmployees INT,
    ebitda INT,
    totalDebt INT,
    totalRevenue INT,
    debtToEquity FLOAT,
    grossMargins FLOAT,
    ebitdaMargins FLOAT,
    PRIMARY KEY (symbol)
);

CREATE TABLE stock_prices(
    symbol VARCHAR(25),
    date DATE,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    volume INT,
    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);
