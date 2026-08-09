% ==========================================
% 推論トレースシステム PoC シミュレーター
% ==========================================

% --- 1. ルールの定義 (Definition 3.1) ---
% rule(RuleName, Head, Premises, Conclusions).

% 例10.1 (人間は死すべきである)
rule(mortal, mortal(X), [human(X)], []).

% 例10.2 (鍵による解錠)
rule(unlock, unlock(X), [key_for(Y, X), has(Y)], [opened(X)]).

% 例10.3 (所有の移動)
rule(give, give(X, Y, O), [have(X, O)], [have(Y, O)]).


% --- 2. 状態遷移と前提消費 (Definition 8.1 - 8.4) ---

% 前提テンプレート列を現在の状態（多重集合）から消費するヘルパー述語
% select/3 を用いることで、リストから要素を1つだけ取り除き（多重集合の性質）、
% 残りの状態を返します。
consume([], State, State).
consume([P|Ps], State, RemainingState) :-
    select(P, State, TempState),
    consume(Ps, TempState, RemainingState).

% 一段遷移 (One-step transition)
% step(現在の状態, 実行対象(Head), 次の状態, 適用されたルール名)
step(State, Action, NextState, RuleName) :-
    % 実行対象(Action)とルールのHeadをマッチング（誘導代入の取得と前提の可充足性確認）
    rule(RuleName, Action, Premises, Conclusions),
    
    % 前提を消費し、Consumedを取り除いた状態(TempState)を得る
    consume(Premises, State, TempState),
    
    % 生成多重集合 (Produced multiset) の決定と次状態の構築
    ( Conclusions = [] ->
        % 結論が空の場合は、実行対象自身を状態に追加する
        NextState = [Action | TempState]
    ;
        % それ以外の場合は、結論テンプレート列を状態に追加する
        append(Conclusions, TempState, NextState)
    ).


% --- 3. 逐次実行 (Definition 9.2) ---
% execute(初期状態, 実行列のリスト, 最終状態).

execute(State, [], State).
execute(State, [Action|Rest], FinalState) :-
    step(State, Action, NextState, _RuleName),
    execute(NextState, Rest, FinalState).
