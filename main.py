def calculate_reward(events: list[tuple[str, int, int]]) -> dict[str, float]:
  user_shares = {}
  user_rewards = {}

  max_timestamp = 0
  reward_per_sec = 2.778
  duration = 3600

  first_winner = ""
  last_winner = ""

  stakeholder = []

  for sec in range(duration):
    for user, timestamp, shere_adjust in events:
      if ( timestamp == sec ): 
        if len(last_winner) == 0:
          if ( shere_adjust >= 1 ):
            user_shares[user] = user_shares.get(user, 0) + shere_adjust
            first_winner = user
            stakeholder.append(user)
        else:
          if ( last_winner != user ):
            stakeholder.append(user)
            time_diff = sec - max_timestamp
            calculate_reward = time_diff * reward_per_sec
            
            if ( shere_adjust >= 1 ):
              user_shares[user] = user_shares.get(user, 0) + shere_adjust

              if ( first_winner == last_winner ):
                user_rewards[last_winner] = user_rewards.get(user, 0) + calculate_reward

            if ( user == first_winner ):
              full_shared = sum(user_shares.values())
              full_reward = time_diff * reward_per_sec

              for user, shares in user_shares.items():
                  user_rate = shares / full_shared
                  user_current_reward = user_rewards.get(user, 0)
                  user_new_reward = user_rate * full_reward
                  user_rewards[user] = user_current_reward + user_new_reward

        if timestamp > max_timestamp:
          max_timestamp = timestamp

      last_winner = user

    if ( sec == duration - 1 ):
      users = list(set(stakeholder))
      total_rewards_diff_between_duration = (duration - max_timestamp) * reward_per_sec
      
      for user in users:
        rate = 1/len(users)
        user_rewards[user] = user_rewards.get(user, 0) + (rate * total_rewards_diff_between_duration)
      return user_rewards

events = [("A", 0, 2), ("B", 2, 1), ("A", 10, -1)]
rewards = calculate_reward(events)

print(f"Rewards: {rewards}")