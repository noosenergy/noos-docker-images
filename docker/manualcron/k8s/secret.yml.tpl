apiVersion: v1
kind: Secret
metadata:
  name: manualcron-dotenv
  namespace: noos-cron
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID:
  AWS_SECRET_ACCESS_KEY:
  RTE_ID64:
---
apiVersion: v1
kind: Secret
metadata:
  name: git-creds
  namespace: noos-cron
type: Opaque
data:
  ssh:
  known_hosts:
