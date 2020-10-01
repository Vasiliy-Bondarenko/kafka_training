# Ethereum Gateway

## Cheatsheet
```sql
-- txs joined 
select * from eth_transactions_submit as s
left join eth_transactions_receive as r on s.id = r.id
where r.id is NULL
limit 100;


-- transactions without responses
select count(*) from eth_transactions_submit as s
left join eth_transactions_receive as r on s.id = r.id
where r.id is NULL;

-- responses without submitted transactions
select count(*) from eth_transactions_receive as r
left join eth_transactions_submit as s on s.id = r.id
where s.id is NULL;

-- search for particular tx id
select * from eth_transactions_submit where id='b464b055-e2c8-4d9b-95a4-3d044d6baa85';
select * from eth_transactions_receive where id='b464b055-e2c8-4d9b-95a4-3d044d6baa85';

-- filter by status
select * from eth_transactions_receive where type != 'TransactionSuccess' limit 100;

-- count rows
select 
	(select count(*) from eth_transactions_submit) as submit,
	(select count(*) from eth_transactions_receive) as receive,
	(select count(*) from logs) as logs;

-- delete all data in a table
delete from eth_transactions_receive where true;
```
