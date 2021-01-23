#!/bin/bash -e
#
# Build a container (optional)
# Then run it.
#
CONTAINER_TAG="simple_python_chat_api:latest"
LISTENER_PORT="0.0.0.0:8080:5000"

showusage(){
  echo "You must specify $0 <build|run>.  You can say build and run at the same time."
  echo "Example:"
  echo "   # $0 build run"
  echo "   # $0 build"
  echo "   # $0 run"
  exit 1
}

if [[ ! -n "$1" ]]; then
  showusage
else
  echo "starting..."
  for i in "$@"; do
    echo "Executing: $i"
    case "$i" in
      "help")
        showusage
        ;;
      "build")
        docker build --tag "$CONTAINER_TAG" .
        ;;
      "run")
        docker run -d --publish "$LISTENER_PORT" "$CONTAINER_TAG"
        echo "..."
        echo "LISTENER: $LISTENER_PORT"
        docker ps
        ;;
      *)
        echo "Syntax error.  Use $0 help for usage."
        exit 1
    esac
  done
fi