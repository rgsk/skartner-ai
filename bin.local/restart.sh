dir="$(dirname "$0")"

sh "$dir/stop.sh"
sh "$dir/build.sh"
sh "$dir/start.sh"