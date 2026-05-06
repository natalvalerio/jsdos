import os
import argparse
from fnmatch import fnmatch

def gitignore_matches(pattern: str, rel_path: str) -> bool:
    """
    Aproximação simples (mas funcional) para matching de .gitignore.
    Funciona bem para padrões comuns em projetos Node.js/Flask (node_modules, dist/, *.log, .env, etc.).
    """
    rel_path = rel_path.replace(os.sep, "/")
    pattern = pattern.strip()
    if not pattern:
        return False

    # Remove leading / (padrão raiz)
    if pattern.startswith("/"):
        pattern = pattern[1:]

    # Se termina com / é padrão de diretório
    is_dir_pattern = pattern.endswith("/")
    if is_dir_pattern:
        pattern = pattern[:-1]

    # Caso 1: padrão sem / → match no nome do arquivo/diretório (recursivo)
    if "/" not in pattern:
        basename = os.path.basename(rel_path)
        if fnmatch(basename, pattern):
            return True
        return False

    # Caso 2: padrão com / → match no caminho relativo completo
    return (
        fnmatch(rel_path, pattern)
        or fnmatch(rel_path + "/", pattern)
        or fnmatch("/" + rel_path, pattern)
    )


def load_gitignore_patterns(root_dir: str):
    """Carrega apenas os padrões de ignore do .gitignore da raiz (padrões ! são tratados na verificação)."""
    gitignore_path = os.path.join(root_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        return []

    patterns = []
    with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def is_ignored(rel_path: str, patterns: list) -> bool:
    """Verifica se o caminho deve ser ignorado respeitando a ordem e os ! do .gitignore."""
    if not patterns:
        return False

    last_match_ignore = None
    for pattern in patterns:
        if pattern.startswith("!"):
            p = pattern[1:].strip()
            ignore_this = False
        else:
            p = pattern.strip()
            ignore_this = True

        if p and gitignore_matches(p, rel_path):
            last_match_ignore = ignore_this

    return last_match_ignore if last_match_ignore is not None else False


def build_tree_and_files(root_dir: str, gitignore_patterns: list):
    """Gera a árvore (apenas itens não ignorados) e lista de arquivos para concatenar."""
    tree_lines = []
    files_to_concat = []  # (rel_path, full_path)

    def walker(current_dir: str, prefix: str = ""):
        try:
            entries = sorted(os.listdir(current_dir))
        except OSError:
            return

        filtered_entries = []
        for entry in entries:
            if entry == ".git":
                continue  # sempre ignora .git

            full_path = os.path.join(current_dir, entry)
            rel_path = os.path.relpath(full_path, root_dir)

            if is_ignored(rel_path, gitignore_patterns):
                continue

            filtered_entries.append(entry)

        # Gera a árvore e coleta arquivos
        for i, entry in enumerate(filtered_entries):
            is_last = i == len(filtered_entries) - 1
            connector = "└── " if is_last else "├── "
            tree_lines.append(prefix + connector + entry)

            full_path = os.path.join(current_dir, entry)
            rel_path = os.path.relpath(full_path, root_dir)

            if os.path.isdir(full_path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                walker(full_path, new_prefix)
            else:
                # Arquivo → será concatenado (tentaremos ler como texto depois)
                files_to_concat.append((rel_path, full_path))

    walker(root_dir)
    tree_str = ".\n" + "\n".join(tree_lines)
    return tree_str, files_to_concat


def concatenate_project(project_dir: str, output_file: str):
    """Função principal: gera árvore + conteúdo dos arquivos."""
    print(f"Processando projeto: {project_dir}")
    
    gitignore_patterns = load_gitignore_patterns(project_dir)
    if gitignore_patterns:
        print(f"✅ .gitignore encontrado ({len(gitignore_patterns)} padrões). Respeitando ignores...")

    tree_str, files_to_concat = build_tree_and_files(project_dir, gitignore_patterns)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("=== ESTRUTURA DO PROJETO (TREE) ===\n\n")
        out.write(tree_str)
        out.write("\n\n")
        out.write("=== CONTEÚDO DOS ARQUIVOS ===\n\n")

        for rel_path, full_path in files_to_concat:
            out.write(f"--- {rel_path}\n")
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                out.write(content)
                out.write("\n\n")
            except UnicodeDecodeError:
                out.write("[Arquivo binário ou codificação inválida - ignorado]\n\n")
            except Exception as e:
                out.write(f"[Erro ao ler o arquivo: {e}]\n\n")

    print(f"✅ Pronto! Arquivo gerado em:")
    print(f"   {os.path.abspath(output_file)}")
    print(f"   Total de arquivos concatenados: {len(files_to_concat)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatena todo o código de um projeto em um único arquivo TXT (respeita .gitignore e ignora .git)"
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Diretório do projeto (padrão: pasta atual)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Nome do arquivo de saída (padrão: project_concatenated.txt dentro do projeto)",
    )

    args = parser.parse_args()

    root = os.path.abspath(args.project_dir)

    if args.output:
        output_file = os.path.abspath(args.output)
    else:
        output_file = os.path.join(root, "projeto.txt")

    concatenate_project(root, output_file)