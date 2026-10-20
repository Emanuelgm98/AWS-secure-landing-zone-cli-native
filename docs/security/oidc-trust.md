# GitHub OIDC trust example

`examples/oidc-trust-policy.json` is a non-active template. Replace every marker, constrain `sub` to the exact immutable repository and protected ref/environment, retain the AWS audience condition, and review repository transfer/fork risks. Create no role or workflow token permission until a separate approved design maps actions to least-privilege IAM permissions. The included GitHub workflows use `contents: read`; none request `id-token: write`, access AWS, or deploy.
