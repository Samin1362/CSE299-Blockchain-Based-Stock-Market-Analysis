// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DSE {
    struct Stock {
        uint256 id;
        string name;
        uint256 price;
        uint256 availableQuantity;
    }

    struct User {
        uint256 id;
        string name;
        uint256 balance;
        mapping(uint256 => uint256) stocksOwned;
    }

    mapping(address => User) public users;
    mapping(uint256 => Stock) public stocks;

    uint256 public nextStockId = 1;
    uint256 public nextUserId = 1;

    event StockAdded(uint256 id, string name, uint256 price, uint256 availableQuantity);
    event StockBought(address buyer, uint256 stockId, uint256 quantity);
    event StockSold(address seller, uint256 stockId, uint256 quantity);

    function addStock(string memory _name, uint256 _price, uint256 _availableQuantity) public {
        stocks[nextStockId] = Stock(nextStockId, _name, _price, _availableQuantity);
        nextStockId++;
        emit StockAdded(nextStockId, _name, _price, _availableQuantity);
    }

    function buyStock(uint256 _stockId, uint256 _quantity) public payable {
        require(stocks[_stockId].availableQuantity >= _quantity, "Not enough available stock quantity to buy");
        uint256 cost = stocks[_stockId].price * _quantity;
        require(users[msg.sender].balance >= cost, "Insufficient balance to buy stock");
        
        users[msg.sender].balance -= cost;
        users[msg.sender].stocksOwned[_stockId] += _quantity;
        stocks[_stockId].availableQuantity -= _quantity;
        
        emit StockBought(msg.sender, _stockId, _quantity);
    }

    function sellStock(uint256 _stockId, uint256 _quantity) public {
        require(users[msg.sender].stocksOwned[_stockId] >= _quantity, "Insufficient stock quantity to sell");
        uint256 revenue = stocks[_stockId].price * _quantity;
        users[msg.sender].balance += revenue;
        users[msg.sender].stocksOwned[_stockId] -= _quantity;
        stocks[_stockId].availableQuantity += _quantity;
        
        emit StockSold(msg.sender, _stockId, _quantity);
    }

    function registerUser(string memory _name) public {
        require(bytes(_name).length > 0, "Name cannot be empty");
        users[msg.sender].id = nextUserId;
        users[msg.sender].name = _name;
        nextUserId++;
    }

    function getUserBalance() public view returns (uint256) {
        return users[msg.sender].balance;
    }

    function increaseUserBalance(address _user, uint256 _amount) public {
    // Add a condition to ensure only authorized users can increase the balance
    // You can use access control mechanisms here.

    // Update the user's balance
        users[_user].balance += _amount;
    }

    function getStocksOwned() public view returns (uint256[] memory) {
        uint256[] memory stocksOwned = new uint256[](nextStockId);

        for (uint256 i = 1; i < nextStockId; i++) {
            stocksOwned[i - 1] = users[msg.sender].stocksOwned[i];
        }

        return stocksOwned;
    }


}
