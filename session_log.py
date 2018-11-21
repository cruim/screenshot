import postgresql
import error_log
import db_conf
import current_stack
import determine_position
import headsup
import image_processing


def insert_into_log_session(screen_area, hand, current_position='0', current_stack='0', action='', is_headsup=0,
                            last_opponent_action=None):
    try:
        db = postgresql.open(db_conf.connection_string())
        data = db.prepare(
            "insert into session_log(screen_area,hand,current_position,current_stack,action,is_headsup,last_opponent_action) "
            "values($1,$2,$3,$4,$5,$6,$7)")
        data(screen_area, hand, current_position, current_stack, action, int(is_headsup), last_opponent_action)
    except Exception as e:
        error_log.error_log('insertIntoLogSession', str(e))
        print(e)


def get_last_row_action_from_log_session(screen_area):
    try:
        db = postgresql.open(db_conf.connection_string())
        sql = "select trim(action) as action from session_log where screen_area = $1 order by id desc limit 1"
        data = db.query.first(sql, int(screen_area))
        return data
    except Exception as e:
        error_log.error_log('getLastRowActionFromLogSession', str(e))
        print(e)


def update_action_log_session(action, screen_area):
    try:
        db = postgresql.open(db_conf.connection_string())
        db.query("UPDATE session_log SET action=yourvalue FROM "
                 "(SELECT id, '" + action + "' AS yourvalue FROM session_log where screen_area = " + screen_area +
                 " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.error_log('updateActionLogSession' + action, str(e))
        print(e)


def get_last_is_flop_log_session(screen_area):
    db = postgresql.open(db_conf.connection_string())
    sql = "select is_flop from session_log where screen_area = $1 order by id desc limit 1"
    data = db.query.first(sql, int(screen_area))
    return data


def update_is_flop_log_session(screen_area):
    db = postgresql.open(db_conf.connection_string())
    db.query("UPDATE session_log SET is_flop = 1 FROM "
             "(SELECT id FROM session_log where screen_area = " + screen_area + "ORDER BY id desc limit 1) "
                                                                                "AS t1 WHERE session_log.id=t1.id")


def update_current_stack_log_session(screen_area, actual_stack):
    try:
        db = postgresql.open(db_conf.connection_string())
        db.query("UPDATE session_log SET current_stack=yourvalue FROM "
                 "(SELECT id, " + actual_stack + "AS yourvalue FROM session_log where screen_area = " +
                 screen_area + " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.error_log('updateCurrentStackLogSession', str(e))
        print(e)


def get_last_row_from_log_session(screen_area):
    try:
        db = postgresql.open(db_conf.connection_string())
        sql = "select trim(hand) as hand,trim(current_stack) as current_stack,trim(current_position) as current_position, " \
              "trim(action) as action, is_headsup, trim(last_opponent_action) as last_opponent_action " \
              "from session_log where screen_area = $1 order by id desc limit 1"
        data = db.query(sql, int(screen_area))
        return data
    except Exception as e:
        error_log.error_log('getLastHandFromLogSession', str(e))
        print(e)


def check_conditions_before_insert(hand, screen_area, stack_collection):
    try:
        position = str(determine_position.seacrh_blind_chips(screen_area))
        stack = current_stack.search_current_stack(screen_area, stack_collection)
        is_headsup = 1
        if int(stack) > 6:
            opponent_data = headsup.search_opponent_card(str(screen_area), stack_collection)
            is_headsup = opponent_data[0]
            opponent_data.pop(0)
            if len(opponent_data) > 0:
                opponent_actual_stack = sorted(opponent_data, reverse=True)
                if int(opponent_actual_stack[0]) == 666:
                    all_in_stack = current_stack.search_allin_stack(screen_area)
                    opponent_actual_stack[0] = all_in_stack
                opponent_actual_stack = max(opponent_actual_stack)
                if int(opponent_actual_stack) < int(stack):
                    stack = opponent_actual_stack
        stack = current_stack.convert_stack(stack)
        if position == 'big_blind' or (position == 'small_blind' and is_headsup == 0):
            last_opponent_action = image_processing.search_last_opponent_action(screen_area)
            last_opponent_action = get_last_opponent_action(position, last_opponent_action)
        else:
            last_opponent_action = None
        insert_into_log_session(screen_area, hand, position, str(stack), is_headsup=is_headsup,
                                last_opponent_action=last_opponent_action)
    except Exception as e:
        error_log.error_log('checkConditionsBeforeInsert', str(e))
        print(e)


def update_hand_after_flop(screen_area, hand):
    db = postgresql.open(db_conf.connection_string())
    db.query("UPDATE session_log SET hand= '" + hand +
             "' from(SELECT id FROM session_log where screen_area = " +
             screen_area + " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id")


def update_hand_after_turn(screen_area, turn):
    db = postgresql.open(db_conf.connection_string())
    db.query("UPDATE session_log SET hand= hand || '" + turn +
             "' from(SELECT id FROM session_log where screen_area = " +
             screen_area + " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id")


def update_hand_value(screen_area, hand_value):
    db = postgresql.open(db_conf.connection_string())
    db.query("UPDATE session_log SET hand_value= '" + hand_value +
             "' from(SELECT id FROM session_log where screen_area = " +
             screen_area + " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id")


def get_hand_value(screen_area):
    db = postgresql.open(db_conf.connection_string())
    sql = "select trim(hand_value) as hand_value from session_log where screen_area = $1 order by id desc limit 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_actual_hand(screen_area):
    db = postgresql.open(db_conf.connection_string())
    sql = "select trim(hand) as hand from session_log where screen_area = $1 order by id desc limit 1"
    data = db.query.first(sql, int(screen_area))
    return data


def update_is_headsup_postflop(screen_area, is_headsup):
    db = postgresql.open(db_conf.connection_string())
    db.query("UPDATE session_log SET is_headsup = " + str(
        is_headsup) + " from(SELECT id FROM session_log where screen_area = " +
             screen_area + " ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id")


def get_last_opponent_action(position, last_opponent_action):
    if isinstance(last_opponent_action, str):
        last_opponent_action = 'push'
    elif position == 'big_blind' and last_opponent_action['alias'] == '1':
        last_opponent_action = 'min_raise'
    elif position == 'big_blind' and last_opponent_action['alias'] in ('2', '3'):
        last_opponent_action = 'open'
    elif position == 'small_blind' and last_opponent_action['alias'] == '2':
        last_opponent_action = 'min_raise'
    elif position == 'small_blind' and last_opponent_action['alias'] == '3':
        last_opponent_action = 'open'
    elif last_opponent_action['alias'] in ('check', '0.5'):
        last_opponent_action = 'limp'
    else:
        last_opponent_action = 'push'
    return last_opponent_action
