IMG_NAME = "asia.gcr.io/alecsharpie/habaneros"

img-build:
	docker build -t ${IMG_NAME} .

img-run:
	docker run --env-file .env -p 8000:8000 ${IMG_NAME}

img-push:
	docker push ${IMG_NAME}

img-deploy:
	gcloud run deploy \
			--image ${IMG_NAME} \
			--platform managed \
			--region asia-east1 \
			--allow-unauthenticated \
			--env-vars-file env.yaml
