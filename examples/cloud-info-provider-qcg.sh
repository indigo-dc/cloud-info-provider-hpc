export TOKEN="*** insert token here***"
export API_URL="http://qcg.lambda.ara.app.test.k8s.apps.psnc.pl/api"
python cloud-info-provider-qcg.py --qcg-url $API_URL --token $TOKEN <header-qcg
