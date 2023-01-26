def get_ssm_parameter(ssmClient, ssmPath, withDecryption):
    parameter = ssmClient.get_parameter(Name=ssmPath, WithDecryption=withDecryption)
    return parameter['Parameter']['Value']