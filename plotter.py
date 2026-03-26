import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import subprocess
import logging
from pathlib import Path
import latexwriter
import general as gen

log = logging.getLogger("app")
scriptdir = Path(__file__).resolve().parent


# -------------------------
# Helper
# -------------------------
def _get_jpg_path(v, D, files):
    jpg_file = gen.modify_filenames(v, D, files)[1]
    full = scriptdir / files / jpg_file
    return str(full).replace("\\", "/")


# -------------------------
# Plot
# -------------------------
def plot_to_jpg(v, D, adm_estimates_and_lines, dyadic_estimates_D, selfadjoint, files):

    jpg_file_full_str = _get_jpg_path(v, D, files)
    print("Start plotting the Riesz diagram to " + jpg_file_full_str)
    log.info("Start plotting the Riesz diagram to " + jpg_file_full_str)

    adm_pts, adm_lines = adm_estimates_and_lines

    # Base plot
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    plt.grid(True)
    plt.suptitle('Riesz diagram')
    plt.xlabel(r"$\frac{1}{p}$", fontsize=15, labelpad=-5)
    plt.ylabel(r"$\frac{1}{q}$", rotation=0, fontsize=15, labelpad=20)

    # Convex regions
    if len(adm_pts) > 2 and len(adm_lines) > 1:

        try:
            hull = ConvexHull([[d[0], d[1]] for d in dyadic_estimates_D])
            pts = [dyadic_estimates_D[i] for i in hull.vertices]
            plt.fill([p[0] for p in pts], [p[1] for p in pts], alpha=0.2)
            log.info("Convex region of admissible estimates resulting from dyadic estimates only is drawn.")
        except:
            plt.fill([0, 1], [0, 0], alpha=0.2)
            log.warning("Dyadic estimates do not provide an open region of validity.")

        try:
            hull = ConvexHull([[p[0], p[1]] for p in adm_pts])
            pts = [adm_pts[i] for i in hull.vertices]
            plt.fill([p[0] for p in pts], [p[1] for p in pts], alpha=0.6)
            log.info("Convex region of admissible estimates is drawn.")
        except:
            log.warning("Estimates do not provide an open region of validity.")

    # Title
    titles = {
        1: r"Weak-type estimates $L^{p,1} \,\to\, L^{q,\infty}$, d = ",
        2: r"Lorentz estimates $L^{p,s} \,\to\, L^{q,s}$, d = ",
        3: r"Weak-Strong estimates $L^{p,1} \,\to\, L^{q}$, d = ",
        4: r"Strong-Weak estimates $L^p \,\to\, L^{q,\infty}$, d = ",
        5: r"Lebesgue estimates $L^p \,\to\, L^q$, d = "
    }
    if v in titles:
        plt.title(titles[v] + str(D))
    log.info("The title of the jpg file is set.")

    if selfadjoint:
        plt.plot([0, 1], [1, 0], color='g', linestyle=':', alpha=0.4)

    # Points
    true_pts = [p for p in adm_pts if p[2]]
    false_pts = [p for p in adm_pts if not p[2]]
    plt.scatter([p[0] for p in true_pts], [p[1] for p in true_pts], s=30, c='black', alpha=1)
    plt.scatter([p[0] for p in false_pts], [p[1] for p in false_pts], s=30, c='r', alpha=1)

    # Special Lebesgue case
    if v == 5:
        for i, line in enumerate(adm_lines):
            next_line = adm_lines[(i + 1) % len(adm_lines)]
            if "A" in line[1][2] and line[1] == next_line[0]:
                if not line[2] or not next_line[2]:
                    plt.scatter([line[1][0]], [line[1][1]], s=30, c='green', alpha=1)
                    log.info("The inserted boundary point" + gen.toString(line[0]) + " (on the diagonal) was added in green color.")
                plt.plot([0, 1], [0, 1], color='g', linestyle=':', alpha=0.2)

    log.info("The points are drawn.")

    # Lines
    for line in adm_lines:
        x = [line[0][0], line[1][0]]
        y = [line[0][1], line[1][1]]
        if line[2]:
            plt.plot(x, y, color='black')
        else:
            plt.plot(x, y, color='red', linestyle='--')

    log.info("The lines are drawn.")
    plt.savefig(jpg_file_full_str, format="jpg")
    log.info("The jpg file is saved as " + jpg_file_full_str + ".")
    plt.close()
    log.info("Plotting to jpg is done.")


# -------------------------
# LaTeX Output
# -------------------------
def output_plot_and_text(v, D, adm_estimates_and_lines, files):

    mapping = {
        1: "Weak-Type",
        2: "Lorentz",
        3: "Weak-Strong",
        4: "Strong-Weak",
        5: "Lebesgue"
    }

    log.info("Having created the jpg create the LaTex code now.")

    jpg_file_full_str = _get_jpg_path(v, D, files)

    try:
        text = []
        text.append(
            r"""\newpage""" + "\n\n" +
            r"""\subsection*{Output data for """ + mapping.get(v) + " estimates, d=" + str(D) + r"""}""" +
            "\n\n" + r"""\medskip""" + "\n\n"
        )
        text.append(
            r"""\begin{center}
   \includegraphics[scale=0.9]{""" + jpg_file_full_str + r"""}
\end{center}  
\medskip
"""
        )

        adm_pts, adm_lines = adm_estimates_and_lines
        exc_pts = [p for p in adm_pts if not p[2]]
        exc_lines = [l for l in adm_lines if not l[2]]

        if len(adm_pts) > 2 and len(adm_lines) > 1:

            try:
                pqconditions = [
                    gen.normalize(eq)
                    for eq in ConvexHull([[p[0], p[1]] for p in adm_pts]).equations
                ]

                eff = [
                    c for c in pqconditions
                    if c not in [[1,0,1],[0,1,1],[-1,0,0],[0,-1,0]]
                    and not gen.is_strict(c, adm_pts, adm_lines)
                ]

                if not eff:
                    text.append(r"""All exponents $p,q\in [1,\infty]$ are admissible.""")
                else:
                    text.append(
                        r"""\noindent The orange region of validity for these estimates is given by all points $(\frac{1}{p},\frac{1}{q})$ that satisfy the 
        following conditions:
        \begin{itemize} 
        \itemsep-2pt 
"""
                    )

                    for cond in pqconditions:
                        if gen.is_strict(cond, adm_pts, adm_lines):
                            text.append(r"""  \item  $""" + latexwriter.latextext(cond, '<>') + "$\n")
                            exc_pts = [p for p in exc_pts if not gen.is_exceptional_pt(p, cond)]
                            exc_lines = [l for l in exc_lines if not gen.is_exceptional_line(l, cond)]
                        elif cond not in [[1,0,1],[0,1,1],[-1,0,0],[0,-1,0]]:
                            text.append(r"""  \item  $""" + latexwriter.latextext(cond, '') + "$\n")

                    text.append(r"""\end{itemize}""" + "\n")

                    if exc_pts or exc_lines:
                        text.append("except for the following points and open segments:\n" +
                                    r"""\begin{itemize}""" + "\n  " + r"""\itemsep-2pt""" + "\n")

                        for pt in exc_pts:
                            text.append(r"""  \item Point  ($""" +
                                        latexwriter.latexsymbolic(pt[0]) + "," +
                                        latexwriter.latexsymbolic(pt[1]) + "$)\n")

                        for line in exc_lines:
                            text.append(r"""  \item Open segment joining  ($""" +
                                        latexwriter.latexsymbolic(line[0][0]) + "," +
                                        latexwriter.latexsymbolic(line[0][1]) + "$)  and  ($" +
                                        latexwriter.latexsymbolic(line[1][0]) + "," +
                                        latexwriter.latexsymbolic(line[1][1]) + "$)\n")

                        text.append(r"""\end{itemize}""" + "\n")

            except:
                text.append(r""" The region of validity is a union of segments:""" + "\n")
                for line in adm_lines:
                    text.append(latexwriter.latexsegment(line[0], line[1]))

                log.warning("The region of validity is a union of segments rather than an open set.")

            log.info("Plot description for convex region is written.")
            return "".join(text)

        elif len(adm_pts) == 2 and len(adm_lines) == 1:

            if adm_lines[0][2]:
                text.append(r""" \noindent The region of validity for these estimates is a segment given as follows:""" + "\n")
                text.append(latexwriter.latexsegment(adm_pts[0], adm_pts[1]))
            else:
                text.append(r""" \noindent The region of validity for is a finite number of points given as follows:""" + "\n")
                text.append(latexwriter.latexpoints(adm_pts))

            return "".join(text)

        else:
            log.error("Unexpected Data")
            exit()

    except:
        log.error("Error while writing the LaTex code for the pdf. End of program!")
        exit()


# -------------------------
# File Output
# -------------------------
def print_and_plot_to_files(text, files):

    log.info("Start printing and plotting to the pdf file with LaTex.")

    texfile = scriptdir / files / (files + ".tex")
    texfile_str = str(texfile).replace("\\", "/")

    with open(texfile, "w", encoding="utf-8") as f:
        f.write(text)

    log.info("The LaTex code is written to " + texfile_str)

    result = subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-output-directory",
            str((scriptdir / files)).replace("\\", "/"),
            files + ".tex"
        ],
        check=True
    )

    if result.returncode == 0:
        log.info("The LaTex code was successfully executed with pdflatex.")
    else:
        log.error("The LaTex code could not be executed with pdflatex.")
        exit()


