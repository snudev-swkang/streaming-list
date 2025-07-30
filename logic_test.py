import random
import itertools

# 이전 단계에서 만든 아이템 리스트를 여기 다시 붙여넣을게!
# 실제 사용 시에는 이 부분이 이전에 생성된 `items` 변수를 바로 활용하면 돼!
items = []
for i in range(1, 11):
    item_name = f"Item {i}"
    # 이번에는 조금 더 30에 가까운 조합이 나올 수 있도록 value 범위를 조정해볼게!
    # 그래도 완전 랜덤이니까, 결과는 달라질 수 있어!
    item_value = random.randint(1, 10)
    item = {
        "name": item_name,
        "value": item_value
    }
    items.append(item)

print("--- 생성된 아이템 목록 ---")
for item in items:
    print(f"- {item['name']}: {item['value']}")
print("--------------------------\n")

# 필수로 포함해야 할 아이템들을 먼저 찾아내자!
required_item_names = ["Item 1", "Item 3", "Item 5"]
required_items = []
remaining_items = [] # 나머지 아이템들

for item in items:
    if item['name'] in required_item_names:
        required_items.append(item)
    else:
        remaining_items.append(item)

# 필수 아이템들이 진짜 3개 다 있는지 확인! 혹시라도 아이템 이름 오타났을까봐 😅
if len(required_items) != len(required_item_names):
    print("🚨 경고: 필수 아이템 중 일부가 아이템 목록에 없거나 이름이 잘못되었어요! ㅠㅠ")
    print(f"  찾으려 했던 필수 아이템: {required_item_names}")
    print(f"  실제로 찾은 필수 아이템: {[item['name'] for item in required_items]}\n")
    # 필수 아이템이 없으면 더 이상 진행할 수 없으니 여기서 종료할 수도 있어!
    # exit() 또는 raise Exception으로 강제 종료 가능

# 필수 아이템들의 초기 밸류 합계를 계산
current_base_sum = sum(item['value'] for item in required_items)
print(f"🎯 필수 아이템 ({', '.join([item['name'] for item in required_items])})의 현재 합계: {current_base_sum}")

exact_matches = [] # 정확히 30이 되는 조합들
best_approx_sum = current_base_sum # 30 이하이면서 30에 가장 가까운 합 (필수 아이템 합으로 초기화)
best_approx_combinations = [] # best_approx_sum에 해당하는 조합들

# 만약 필수 아이템들의 합이 이미 30이 넘으면, 30 이하 조합은 나올 수 없어
if current_base_sum > 30:
    print(f"⚠️ 필수 아이템들의 합이 이미 목표(30)를 초과했어요! (현재 합: {current_base_sum})")
    print("30 이하이면서 가까운 조합을 찾기 어려울 수 있습니다. 이 조합 자체는 30 초과입니다.")
    # 이 경우, 필수 아이템만으로 이루어진 조합을 가장 가까운 조합으로 간주할 수 있음
    best_approx_sum = current_base_sum # 이 경우 초과한 값이라도 이 조합이 최선일 수 있음
    best_approx_combinations = [{
        "items": [item['name'] for item in required_items],
        "total_value": current_base_sum
    }]

# 이제 나머지 아이템들로 조합을 만들어서 필수 아이템과 합쳐볼 거야!
# 나머지 아이템에서 0개부터 남은 모든 아이템을 선택하는 경우의 수!
for r in range(0, len(remaining_items) + 1):
    for combo_rest in itertools.combinations(remaining_items, r):
        # 필수 아이템 + 나머지 아이템으로 구성된 최종 조합
        current_full_combo = list(required_items) + list(combo_rest)
        current_sum = sum(item['value'] for item in current_full_combo)
        item_names = [item['name'] for item in current_full_combo]

        if current_sum == 30:
            # 중복 저장을 막기 위해, 이미 추가된 조합인지 확인
            # (item_names를 정렬해서 문자열로 비교하는 방법 등)
            # 여기서는 일단 간단하게 추가할게. 더 복잡한 중복 제거는 나중에 필요하면 추가하자!
            exact_matches.append({
                "items": sorted(item_names), # 이름으로 정렬해서 보기 좋게!
                "total_value": current_sum
            })
        elif current_sum < 30:
            if current_sum > best_approx_sum:
                best_approx_sum = current_sum
                best_approx_combinations = [{
                    "items": sorted(item_names),
                    "total_value": current_sum
                }]
            elif current_sum == best_approx_sum:
                # 같은 합계를 가진 조합이 여러 개 나올 수 있으니 리스트에 추가
                best_approx_combinations.append({
                    "items": sorted(item_names),
                    "total_value": current_sum
                })

# 중복 조합 제거 (정확히 30인 경우)
# set을 활용해서 중복을 제거할 수 있어!
unique_exact_matches = []
seen_exact_combos = set()
for match in exact_matches:
    combo_str = tuple(match['items']) # 리스트를 튜플로 변환해야 set에 넣을 수 있어
    if combo_str not in seen_exact_combos:
        seen_exact_combos.add(combo_str)
        unique_exact_matches.append(match)

# 중복 조합 제거 (가장 가까운 경우)
unique_best_approx_combinations = []
seen_approx_combos = set()
for combo in best_approx_combinations:
    combo_str = tuple(combo['items'])
    if combo_str not in seen_approx_combos:
        seen_approx_combos.add(combo_str)
        unique_best_approx_combinations.append(combo)

print("\n--- 조건부 조합 결과 (Item 1, Item 3, Item 5 필수 포함) ---")

if unique_exact_matches:
    print("✨ 정확히 밸류 총합이 30인 조합을 찾았어! ✨")
    for match in unique_exact_matches:
        print(f"  조합: {', '.join(match['items'])} (총합: {match['total_value']})")
else:
    print("😔 정확히 밸류 총합이 30인 조합은 없네...")
    if unique_best_approx_combinations:
        # best_approx_sum이 필수 아이템만으로도 30을 넘겼을 경우
        if current_base_sum > 30 and best_approx_sum == current_base_sum:
            print(f"⚠️ 필수 아이템들의 합이 이미 목표(30)를 초과하여,")
            print(f"   필수 아이템만으로 구성된 조합이 현재로서 가장 가까운 조합이에요! (총합: {current_base_sum})")
            print(f"   조합: {', '.join([item['name'] for item in required_items])}")
        else:
            print(f"가장 30에 가까우면서 30 이하인 조합들을 찾아봤어! (최대 총합: {best_approx_sum})")
            for combo in unique_best_approx_combinations:
                print(f"  조합: {', '.join(combo['items'])} (총합: {combo['total_value']})")
    else:
        print("이런, 필수 아이템을 포함하면서 30 이하인 조합 자체를 찾을 수 없었어 ㅠㅠ")

print("----------------------------------------------------------------\n")