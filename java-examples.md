# Java SDK Examples

## Intro

Run examples from <https://github.com/awsdocs/aws-doc-sdk-examples>.

## Cloud

Create Cloud9 environment and open a terminal.

## Install Examples

```bash
# Install maven.
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
mvn --version

# Grab and build SDK examples.
git clone https://github.com/awsdocs/aws-doc-sdk-examples.git
cd aws-doc-sdk-examples/java/example_code

# Build examples for DynamoDB.
cd dynamodb
make

# View examples
ls src/main/java/aws/example/dynamodb/
```

## Output

```
CreateTableCompositeKey.java
CreateTable.java
DeleteItem.java
DeleteTable.java
DescribeTable.java
GetItem.java
ListTables.java
PutItem.java
Query.java
UpdateItem.java
UpdateTable.java
```

## Run Examples

```bash
./run_example.sh CreateTable users                                                             
```
