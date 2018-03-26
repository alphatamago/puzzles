"""
Solver for puzzles like this one:
"You have a can with 12 liters of gasoline and two empty containers of 9 and 5
liters. Separate the whole gasoline in two equal parts."

Source for the puzzle:
https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fandrei.alexandrescu%2Fposts%2F10212907917346199
"""

from collections import deque

def reconstruct_solution(state, visited):
    state_sequence = [state]
    while True:
        try:
            prev = visited[state]
        except:
            prev = None
        if prev is None:
            break
        else:
            state_sequence.append(prev)
            state = prev
    state_sequence.reverse()
    return state_sequence

def next_states(state):
    # For each recipient A that is non-empty, possible actions consist of
    # chosing a recipient B that is not full and pour as much as possible of
    # A into B.
    # It is possible that A goes completely into B (and becomes empty), or
    # A goes partially into B.
    for i in range(len(state)):
        assert state[i][1] >= 0 and state[i][1] <= state[i][0]
        # Looking for a "source recipient"
        # Skipping if empty
        if state[i][1] < 1: continue
        for j in range(len(state)):
            if i == j: continue
            # Looking for a "destination recipient"
            # Skipping if full
            if state[j][1] == state[j][0]: continue
            # delta is the amount we move from i to j
            delta = min(state[i][1], state[j][0] - state[j][1])
            assert delta > 0
            from_recipient = [(state[i][0], state[i][1] - delta)]
            to_recipient = [(state[j][0], state[j][1] + delta)]
            
            state2 = list(state)[:]
            # We don't know if i is before or after j, so we replace twice
            state2 =  state2[:i] + from_recipient + state2[i+1:]
            state2 =  state2[:j] + to_recipient + state2[j+1:]
            yield tuple(state2)


def run(start, end):
    """
    Each of start and end states is a state of the water recipients.
    A state is a list of pairs of numbers, where each pair represents:
    (recipient_volume, water_in_recipient)
    For instance, (12, 12) means we have a recipient of volume 12 and it is
    full, while (9, 0) is for a recipient of volumne 9 which is empty.
    
    We want to find a sequence of actions (consisting of moving the water
    between the recipients) that gets us from the start state to the end state.
    """

    # In the queue we have states to be explored next.
    # For each we also keep the previous state that led to it, to reconstruct
    # the final solution.
    queue = deque([(start, None)])
    visited = {}
    while queue:
        state, prev_state = queue.pop()
        if state == end:
            # We just add to visited for ease of reconstructing the path.
            visited[end] = prev_state
            print("Solution. Sizes:")
            print ([k[0] for k in start])
            print("Sequence of states:")
            for s in reconstruct_solution(state, visited):
                print([k[1] for k in s])
            return
        if state not in visited:
            # Explore this state, find all possible direct next states
            for next_state in next_states(state):
                if next_state not in visited:
                    # Adding on the left side and poping from the right side
                    # for BFS traversal, which gives us shortest path
                    queue.appendleft((next_state, state))
            assert state not in visited
            visited[state] = prev_state
    print("No solution.")

if __name__ == "__main__":
    run(start=((12, 12), (9, 0), (5, 0)),
        end=((12, 6), (9, 6), (5, 0)))
