def export(node, filename):
    def node_to_tikz(node, indent=""):
        if not node:
            return f"{indent}child[missing] {{}}\n", True

        node_text = f"{indent}node {{{node.key}}}"

        children_text = ""
        if node.left or node.right:
            children_text += " {"
            if node.left:
                left_text, _ = node_to_tikz(node.left, indent + "  ")
                children_text += "\n" + left_text
            else:
                children_text += "\n" + f"{indent}  child[missing] {{}}"

            if node.right:
                right_text, _ = node_to_tikz(node.right, indent + "  ")
                children_text += "\n" + right_text
            else:
                children_text += "\n" + f"{indent}  child[missing] {{}}"
            children_text += "\n" + indent + "}"

        return f"{node_text}{children_text}", False

    tikz_output, _ = node_to_tikz(node)
    tikz_string = "\\begin{TikzTreeStyle}\n"
    tikz_string += tikz_output + "\n"
    tikz_string += "\\path[draw=none] (0,-3) -- (0,4mm); % Set tikzpicture height to 34mm\n"
    tikz_string += "\\end{TikzTreeStyle}"

    with open(filename, 'w') as file:
        file.write(tikz_string)
