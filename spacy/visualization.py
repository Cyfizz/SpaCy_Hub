from os import linesep, truncate
from typing import Union
import wasabi
from spacy.tests.lang.ko.test_tokenizer import FULL_TAG_TESTS
from spacy.tokens import Span, Token, Doc
from spacy.util import working_dir


class AttributeFormat:
    def __init__(
        self,
        attribute: str,
        *,
        name: str = "",
        aligns: str = "l",
        max_width: int = None,
        fg_color: Union[str, int] = None,
        bg_color: Union[str, int] = None,
        permitted_values: tuple = None,
        value_dependent_fg_colors: dict[str, Union[str, int]] = None,
        value_dependent_bg_colors: dict[str, Union[str, int]] = None,
    ):
        self.attribute = attribute
        self.name = name
        self.aligns = aligns
        self.max_width = max_width
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.permitted_values = permitted_values
        self.value_dependent_fg_colors = value_dependent_fg_colors
        self.value_dependent_bg_colors = value_dependent_bg_colors


SPACE = 0
HALF_HORIZONTAL_LINE = 1  # the half is the half further away from the root
FULL_HORIZONTAL_LINE = 3
UPPER_HALF_VERTICAL_LINE = 4
LOWER_HALF_VERTICAL_LINE = 8
FULL_VERTICAL_LINE = 12
ARROWHEAD = 16

ROOT_RIGHT_CHARS = {
    SPACE: " ",
    FULL_HORIZONTAL_LINE: "═",
    UPPER_HALF_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╝",
    UPPER_HALF_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╩",
    LOWER_HALF_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╗",
    LOWER_HALF_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╦",
    FULL_VERTICAL_LINE: "║",
    FULL_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╣",
    FULL_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╬",
    ARROWHEAD: "<",
}

ROOT_LEFT_CHARS = {
    SPACE: " ",
    FULL_HORIZONTAL_LINE: "═",
    UPPER_HALF_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╚",
    UPPER_HALF_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╩",
    LOWER_HALF_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╔",
    LOWER_HALF_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╦",
    FULL_VERTICAL_LINE: "║",
    FULL_VERTICAL_LINE + HALF_HORIZONTAL_LINE: "╠",
    FULL_VERTICAL_LINE + FULL_HORIZONTAL_LINE: "╬",
    ARROWHEAD: ">",
}


class Visualizer:
    def __init__(self):
        self.printer = wasabi.Printer(no_print=True)

    @staticmethod
    def render_dependency_tree(sent: Span, root_right: bool) -> list[str]:
        """
        Returns an ASCII rendering of the document with a dependency tree for each sentence. The
        dependency tree output for a given token has the same index within the output list of
        strings as that token within the input document.

        root_right: True if the tree should be rendered with the root on the right-hand side,
                    False if the tree should be rendered with the root on the left-hand side.

        Adapted from https://github.com/KoichiYasuoka/deplacy
        """

        # Check sent is really a sentence
        assert sent.start == sent[0].sent.start
        assert sent.end == sent[0].sent.end
        heads = [
            None
            if token.dep_.lower() == "root" or token.head.i == token.i
            else token.head.i - sent.start
            for token in sent
        ]
        # Check there are no head references outside the sentence
        assert (
            len(
                [
                    head
                    for head in heads
                    if head is not None and (head < 0 or head > sent.end - sent.start)
                ]
            )
            == 0
        )
        children_lists = [[] for _ in range(sent.end - sent.start)]
        for child, head in enumerate(heads):
            if head is not None:
                children_lists[head].append(child)
        all_indices_ordered_by_column = []
        # start with the root column
        indices_in_current_column = [i for i, h in enumerate(heads) if h is None]
        while len(indices_in_current_column) > 0:
            assert (
                len(
                    [
                        i
                        for i in indices_in_current_column
                        if i in all_indices_ordered_by_column
                    ]
                )
                == 0
            )
            all_indices_ordered_by_column = (
                indices_in_current_column + all_indices_ordered_by_column
            )
            indices_in_next_column = []
            # The calculation order of the horizontal lengths of the children
            # on either given side of a head must ensure that children
            # closer to the head are processed first.
            for index_in_current_column in indices_in_current_column:
                following_children_indices = [
                    i
                    for i in children_lists[index_in_current_column]
                    if i > index_in_current_column
                ]
                indices_in_next_column.extend(following_children_indices)
                preceding_children_indices = [
                    i
                    for i in children_lists[index_in_current_column]
                    if i < index_in_current_column
                ]
                preceding_children_indices.reverse()
                indices_in_next_column.extend(preceding_children_indices)
            indices_in_current_column = indices_in_next_column
        horizontal_line_lengths = [
            -1 if heads[i] is None else 1
            # length == 1: governed by direct neighbour and has no children itself
            if len(children_lists[i]) == 0 and abs(heads[i] - i) == 1 else 0
            for i in range(sent.end - sent.start)
        ]
        while 0 in horizontal_line_lengths:
            for working_token_index in (
                i
                for i in all_indices_ordered_by_column
                if horizontal_line_lengths[i] == 0
            ):
                # render relation between this token and its head
                first_index_in_relation = min(
                    working_token_index,
                    heads[working_token_index],
                )
                second_index_in_relation = max(
                    working_token_index,
                    heads[working_token_index],
                )
                # If this token has children, they will already have been rendered.
                # The line needs to be one character longer than the longest of the
                # children's lines.
                if len(children_lists[working_token_index]) > 0:
                    horizontal_line_lengths[working_token_index] = (
                        max(
                            [
                                horizontal_line_lengths[i]
                                for i in children_lists[working_token_index]
                            ]
                        )
                        + 1
                    )
                else:
                    horizontal_line_lengths[working_token_index] = 1
                for inbetween_index in (
                    i
                    for i in range(
                        first_index_in_relation + 1, second_index_in_relation
                    )
                    if horizontal_line_lengths[i] != 0
                ):
                    horizontal_line_lengths[working_token_index] = max(
                        horizontal_line_lengths[working_token_index],
                        horizontal_line_lengths[inbetween_index]
                        if inbetween_index in children_lists[heads[working_token_index]]
                        and inbetween_index not in children_lists[working_token_index]
                        else horizontal_line_lengths[inbetween_index] + 1,
                    )
        max_horizontal_line_length = max(horizontal_line_lengths)
        char_matrix = [
            [SPACE] * max_horizontal_line_length * 2
            for _ in range(sent.start, sent.end)
        ]
        for working_token_index in range(sent.end - sent.start):
            head_token_index = heads[working_token_index]
            if head_token_index is None:
                continue
            first_index_in_relation = min(working_token_index, head_token_index)
            second_index_in_relation = max(working_token_index, head_token_index)
            char_horizontal_line_length = (
                2 * horizontal_line_lengths[working_token_index]
            )

            # Draw the corners of the relation
            char_matrix[first_index_in_relation][char_horizontal_line_length - 1] |= (
                HALF_HORIZONTAL_LINE + LOWER_HALF_VERTICAL_LINE
            )
            char_matrix[second_index_in_relation][char_horizontal_line_length - 1] |= (
                HALF_HORIZONTAL_LINE + UPPER_HALF_VERTICAL_LINE
            )

            # Draw the horizontal line for the governing token
            for working_horizontal_position in range(char_horizontal_line_length - 1):
                if (
                    char_matrix[head_token_index][working_horizontal_position]
                    != FULL_VERTICAL_LINE
                ):
                    char_matrix[head_token_index][
                        working_horizontal_position
                    ] |= FULL_HORIZONTAL_LINE

            # Draw the vertical line for the relation
            for working_vertical_position in range(
                first_index_in_relation + 1, second_index_in_relation
            ):
                if (
                    char_matrix[working_vertical_position][
                        char_horizontal_line_length - 1
                    ]
                    != FULL_HORIZONTAL_LINE
                ):
                    char_matrix[working_vertical_position][
                        char_horizontal_line_length - 1
                    ] |= FULL_VERTICAL_LINE
        for working_token_index in (
            i for i in range(sent.end - sent.start) if heads[i] is not None
        ):
            for working_horizontal_position in range(
                2 * horizontal_line_lengths[working_token_index] - 2, -1, -1
            ):
                if (
                    (
                        char_matrix[working_token_index][working_horizontal_position]
                        == FULL_VERTICAL_LINE
                    )
                    and working_horizontal_position > 1
                    and char_matrix[working_token_index][
                        working_horizontal_position - 2
                    ]
                    == SPACE
                ):
                    # Cross over the existing vertical line, which is owing to a non-projective tree
                    continue
                if (
                    char_matrix[working_token_index][working_horizontal_position]
                    != SPACE
                ):
                    # Draw the arrowhead to the right of what is already there
                    char_matrix[working_token_index][
                        working_horizontal_position + 1
                    ] = ARROWHEAD
                    break
                if working_horizontal_position == 0:
                    # Draw the arrowhead at the boundary of the diagram
                    char_matrix[working_token_index][
                        working_horizontal_position
                    ] = ARROWHEAD
                else:
                    # Fill in the horizontal line for the governed token
                    char_matrix[working_token_index][
                        working_horizontal_position
                    ] |= FULL_HORIZONTAL_LINE
        if root_right:
            return [
                "".join(
                    ROOT_RIGHT_CHARS[
                        char_matrix[vertical_position][horizontal_position]
                    ]
                    for horizontal_position in range((max_horizontal_line_length * 2))
                )
                for vertical_position in range(sent.end - sent.start)
            ]
        else:
            return [
                "".join(
                    ROOT_LEFT_CHARS[char_matrix[vertical_position][horizontal_position]]
                    for horizontal_position in range((max_horizontal_line_length * 2))
                )[::-1]
                for vertical_position in range(sent.end - sent.start)
            ]

    def get_entity(
        self,
        token: Token,
        entity_name: str,
        *,
        permitted_values: list[str] = None,
        value_dependent_fg_colors: dict[str : Union[str, int]] = None,
        value_dependent_bg_colors: dict[str : Union[str, int]] = None,
        truncate_at_width: int = None,
    ) -> str:
        obj = token
        parts = entity_name.split(".")
        for part in parts[:-1]:
            obj = getattr(obj, part)
        value = str(getattr(obj, parts[-1]))
        if permitted_values is not None and value not in (str(v) for v in permitted_values):
            return ""
        if truncate_at_width is not None:
            value = value[:truncate_at_width]
        fg_color = (
            value_dependent_fg_colors.get(value, None)
            if value_dependent_fg_colors is not None
            else None
        )
        bg_color = (
            value_dependent_bg_colors.get(value, None)
            if value_dependent_bg_colors is not None
            else None
        )
        if fg_color is not None or bg_color is not None:
            value = self.printer.text(value, color=fg_color, bg_color=bg_color)
        return value

    def render_table(
        self, doc: Doc, columns: list[AttributeFormat], spacing: int = 3
    ) -> str:
        return_string = ""
        for sent in doc.sents:
            if "tree_right" in (c.attribute for c in columns):
                tree_right = self.render_dependency_tree(sent, True)
            if "tree_left" in (c.attribute for c in columns):
                tree_left = self.render_dependency_tree(sent, False)
            widths = []
            for column in columns:
                # get the values without any color codes
                if column.attribute == "tree_left":
                    width = len(tree_left[0])
                elif column.attribute == "tree_right":
                    width = len(tree_right[0])
                else:
                    width = max(
                        len(
                            self.get_entity(
                                token, column.attribute, permitted_values=column.permitted_values
                            )
                        )
                        for token in sent
                    )
                    if column.max_width is not None:
                        width = min(width, column.max_width)
                width = max(width, len(column.name))
                widths.append(width)
            data = [
                [
                    tree_right[token_index]
                    if column.attribute == "tree_right"
                    else tree_left[token_index]
                    if column.attribute == "tree_left"
                    else self.get_entity(
                        token,
                        column.attribute,
                        permitted_values=column.permitted_values,
                        value_dependent_fg_colors=column.value_dependent_fg_colors,
                        value_dependent_bg_colors=column.value_dependent_bg_colors,
                        truncate_at_width=widths[column_index],
                    )
                    for column_index, column in enumerate(columns)
                ]
                for token_index, token in enumerate(sent)
            ]
            if len([1 for c in columns if len(c.name) > 0]) > 0:
                header = [c.name for c in columns]
            else:
                header = None
            aligns = [c.aligns for c in columns]
            fg_colors = [c.fg_color for c in columns]
            bg_colors = [c.bg_color for c in columns]
            return_string += (
                wasabi.table(
                    data,
                    header=header,
                    divider=True,
                    aligns=aligns,
                    widths=widths,
                    fg_colors=fg_colors,
                    bg_colors=bg_colors,
                    spacing=spacing,
                )
                + linesep
            )
        return return_string
