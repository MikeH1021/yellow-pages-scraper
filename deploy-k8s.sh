#!/bin/bash
set -e

# Yellow Pages Scraper - k3s Deployment Script
# Usage: ./deploy-k8s.sh [build|deploy|all|status|logs|scale]

REGISTRY="${REGISTRY:-}"  # Set to your registry, e.g., "registry.yourdomain.com/"
NAMESPACE="yp-scraper"

build_images() {
    echo "=== Building Docker images ==="

    echo "Building web image..."
    docker build -f Dockerfile.web -t ${REGISTRY}yp-scraper-web:latest .

    echo "Building worker image..."
    docker build -f Dockerfile.worker -t ${REGISTRY}yp-scraper-worker:latest .

    if [ -n "$REGISTRY" ]; then
        echo "Pushing to registry..."
        docker push ${REGISTRY}yp-scraper-web:latest
        docker push ${REGISTRY}yp-scraper-worker:latest
    fi

    echo "=== Images built successfully ==="
}

deploy() {
    echo "=== Deploying to k3s ==="

    # Apply in order: namespace -> secrets/config -> storage -> redis -> app
    kubectl apply -f k8s/namespace.yaml
    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/pvc.yaml
    kubectl apply -f k8s/redis.yaml

    echo "Waiting for Redis..."
    kubectl -n $NAMESPACE rollout status deployment/redis --timeout=60s

    kubectl apply -f k8s/web.yaml
    kubectl apply -f k8s/worker.yaml
    kubectl apply -f k8s/ingress.yaml

    echo "Waiting for web..."
    kubectl -n $NAMESPACE rollout status deployment/web --timeout=120s

    echo "Waiting for workers..."
    kubectl -n $NAMESPACE rollout status deployment/worker --timeout=120s

    echo "=== Deployment complete ==="
    status
}

status() {
    echo "=== Cluster Status ==="
    kubectl -n $NAMESPACE get pods -o wide
    echo ""
    kubectl -n $NAMESPACE get svc
    echo ""
    kubectl -n $NAMESPACE get ingress
}

logs() {
    component="${1:-web}"
    kubectl -n $NAMESPACE logs -l app=$component --tail=50 -f
}

scale_workers() {
    count="${1:-2}"
    echo "Scaling workers to $count..."
    kubectl -n $NAMESPACE scale deployment/worker --replicas=$count
}

case "${1:-all}" in
    build)
        build_images
        ;;
    deploy)
        deploy
        ;;
    all)
        build_images
        deploy
        ;;
    status)
        status
        ;;
    logs)
        logs "$2"
        ;;
    scale)
        scale_workers "$2"
        ;;
    *)
        echo "Usage: $0 [build|deploy|all|status|logs|scale]"
        echo ""
        echo "  build   - Build Docker images"
        echo "  deploy  - Deploy to k3s cluster"
        echo "  all     - Build and deploy (default)"
        echo "  status  - Show pod/service status"
        echo "  logs    - View logs (usage: logs [web|worker|redis])"
        echo "  scale   - Scale workers (usage: scale 3)"
        exit 1
        ;;
esac
