# AWS Cheatsheet

Asim Jalis     
<asimjali@amazon.com>

<!-- vim: set tw=9999: -->

Service | Description
------- | -----------
License Manager | Tracks licenses across EC2 instances and on-prem servers. Enable on AMI. Or enable through Service Manager.
Landing Zone | Solution that helps customers more quickly set up a secure, multi-account AWS environment based on AWS best practices.
Control Tower | Set up and govern a new, secure, multi-account AWS environment based on best practices.
Security Hub | Comprehensive view of high-priority security alerts and compliance status across AWS accounts. 
Route53 Resolver | Inbound query capability allows DNS queries that originate on-premises to resolve AWS hosted domains. Outbound queries that original on AWS use Conditional Forwarding Rules to resolve on-premises domains.
CodeCommit | Git-based source control service.
CodeDeploy | Fully managed serverless deployment service. Deploys to EC2, Fargate, Lambda, on-premises servers. Enables incremental deployment through rolling upgrade to percentage of servers at a time.
CodeBuild | Fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy. Pricing based on instance size used.
CodePipeline | Integrates build, test, deploy process. 
OpsWorks | Managed Chef or Puppet.
CloudHSM | Cloud-based hardware security module (HSM) that enables you to easily generate and use your own encryption keys on the AWS Cloud. With CloudHSM, you can manage your own encryption keys using FIPS 140-2 Level 3 validated HSMs.
