from zxcvbn.scoring import START_UPPER, ALL_UPPER
from gettext import gettext as _


def get_feedback(score, sequence):
    if len(sequence) == 0:
        return {
            'warning': '',
            'suggestions': [
                _("Use a few words, avoid common phrases."),
                _("No need for symbols, digits, or uppercase letters.")
            ]
        }

    if score > 2:
        return {
            'warning': '',
            'suggestions': [],
        }

    longest_match = sequence[0]
    for match in sequence[1:]:
        if len(match['token']) > len(longest_match['token']):
            longest_match = match

    feedback = get_match_feedback(longest_match, len(sequence) == 1)
    extra_feedback = _('Dodaj kilka słów, nietypowe słowa będą lepsze')
    if feedback:
        feedback['suggestions'].insert(0, extra_feedback)
        if not feedback['warning']:
            feedback['warning'] = ''
    else:
        feedback = {
            'warning': '',
            'suggestions': [extra_feedback]
        }

    return feedback


def get_match_feedback(match, is_sole_match):
    if match['pattern'] == 'dictionary':
        return get_dictionary_match_feedback(match, is_sole_match)
    elif match['pattern'] == 'spatial':
        if match['turns'] == 1:
            warning = _('linie, kolumny z klawiatury są łatwe do zgadnięcia.')
        else:
            warning = _('Krótkie wzory z klawiatury nie są najepsze.')

        return {
            'warning': warning,
            'suggestions': [
                _('Użyj dłuższego wzoru klawiatury.')
            ]
        }
    elif match['pattern'] == 'repeat':
        if len(match['base_token']) == 1:
            warning = _('Repeats like "aaa" are easy to guess.')
        else:
            warning = _('Powtórzenia typu "abcabcabc" są tylko nieco trudniejsze ' \
                        'do zgadnięcia niż "abc".')
        return {
            'warning': warning,
            'suggestions': [
                _('unikaj powtarzania.')
            ]
        }
    elif match['pattern'] == 'sequence':
        return {
            'warning': _('Sekfencje takie jak "abc" lub "6543" są łatwe do odgadnięcia'),
            'suggestions': [
                _('unikaj sekfencji.')
            ]
        }
    elif match['pattern'] == 'date':
        return {
            'warning': _("daty są łatwe do odgadnięcia."),
            'suggestions': [
                _('Unikaj dat powiązanych z tobą.'),
            ],
        }


def get_dictionary_match_feedback(match, is_sole_match):
    warning = ''
    if match['dictionary_name'] == 'passwords':
        if is_sole_match and not match.get('l33t', False) and not \
                match['reversed']:
            if match['rank'] <= 10:
                warning = _('To hasło jest w 10 częso używanych haseł.')
            elif match['rank'] <= 100:
                warning = _('To hasło jest w 100 częso używanych haseł.')
            else:
                warning = _('bardzo częste hasło')
        elif match['guesses_log10'] <= 4:
            warning = _('bardzo podobne do często używanego hasła')
    elif match['dictionary_name'] == 'english_wikipedia':
        if is_sole_match:
            warning = _('Samo słowo jest łate do odgadnięcia')
    elif match['dictionary_name'] in ['surnames', 'male_names',
                                      'female_names', ]:
        if is_sole_match:
            warning = _('Same imiona i nazwiska są łatwe do odganięcia.')
        else:
            warning = _('Imiona i nazwiska są łate do odganięcia..')
    else:
        warning = ''

    suggestions = []
    word = match['token']
    if START_UPPER.search(word):
        suggestions.append(_("Duże litery nie pomagają zbytnio."))
    elif ALL_UPPER.search(word) and word.lower() != word:
        suggestions.append(_('Hasło QWERTY jest tak samo łatwe do odganięcia jak qwerty'))

    if match['reversed'] and len(match['token']) >= 4:
        suggestions.append(_("Odwócone wyrazy nie są trudne do odganięcia"))
    if match.get('l33t', False):
        suggestions.append(_("Przewidywalne zamiany, takie jak '@' zamiast 'a' nie pomagają zbytnio."))

    return {
        'warning': warning,
        'suggestions': suggestions,
    }
