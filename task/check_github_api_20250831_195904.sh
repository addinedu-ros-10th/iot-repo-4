set -euo pipefail
out_api="task/url_api_status_$(date +%Y%m%d_%H%M%S).tsv"
printf "http_code\towner\trepo\tdefault_branch\tprivate\n" > "$out_api"
urls=(
https://github.com/addinedu-ros-4th/iot-repo-1
https://github.com/addinedu-ros-4th/iot-repo-2
https://github.com/addinedu-ros-4th/iot-repo-3
https://github.com/addinedu-ros-4th/iot-repo-4
https://github.com/addinedu-ros-4th/iot-repo-5
https://github.com/addinedu-ros-4th/iot-repo-6
https://github.com/addinedu-ros-5th/iot-repo-1
https://github.com/addinedu-ros-5th/iot-repo-2
https://github.com/addinedu-ros-5th/iot-repo-3
https://github.com/addinedu-ros-5th/iot-repo-4
https://github.com/addinedu-ros-5th/iot-repo-5
https://github.com/addinedu-ros-6th/iot-repo-1
https://github.com/addinedu-ros-6th/iot-repo-2
https://github.com/addinedu-ros-6th/iot-repo-3
https://github.com/addinedu-ros-6th/iot-repo-4
https://github.com/addinedu-ros-6th/iot-repo-5
https://github.com/addinedu-ros-6th/iot-repo-6
https://github.com/addinedu-ros-7th/iot-repo-1
https://github.com/addinedu-ros-7th/iot-repo-2
https://github.com/addinedu-ros-7th/iot-repo-3
https://github.com/addinedu-ros-7th/iot-repo-4
https://github.com/addinedu-ros-7th/iot-repo-5
https://github.com/addinedu-ros-8th/iot-repo-1
https://github.com/addinedu-ros-8th/iot-repo-2
https://github.com/addinedu-ros-8th/iot-repo-3
https://github.com/addinedu-ros-8th/iot-repo-4
https://github.com/addinedu-ros-8th/iot-repo-5
https://github.com/addinedu-ros-8th/iot-repo-6
https://github.com/addinedu-ros-9th/iot-repo-1
https://github.com/addinedu-ros-9th/iot-repo-2
https://github.com/addinedu-ros-9th/iot-repo-3
https://github.com/addinedu-ros-9th/iot-repo-4
)
for u in "${urls[@]}"; do
  owner=$(echo "$u" | awk -F/ '{print $4}')
  repo=$(echo "$u" | awk -F/ '{print $5}')
  api="https://api.github.com/repos/${owner}/${repo}"
  tmp="task/_api_${owner}_${repo}.json"
  code=$(curl -sS -H "Accept: application/vnd.github+json" -o "$tmp" -w "%{http_code}" "$api") || true
  def_branch=$(grep -o '"default_branch":"[^"]*"' "$tmp" | head -n1 | sed 's/.*:"\([^"]*\)"/\1/' || true)
  is_private=$(grep -o '"private":\(true\|false\)' "$tmp" | head -n1 | sed 's/.*://')
  printf "%s\t%s\t%s\t%s\t%s\n" "$code" "$owner" "$repo" "${def_branch:-}" "${is_private:-}" >> "$out_api"
done
printf "\nWrote: %s\n" "$out_api"
