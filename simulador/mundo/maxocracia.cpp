#include <array>
#include <algorithm>
#include <cctype>
#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <random>
#include <sstream>
#include <string>
#include <vector>

namespace maxo {

struct SDV {
    double cuerpo = 75.0;
    double relacion = 75.0;
    double sentido = 75.0;
    double promedio() const { return (cuerpo + relacion + sentido) / 3.0; }
    bool en_piso() const { return cuerpo >= 30.0 && relacion >= 30.0 && sentido >= 30.0; }
};

struct Persona {
    int id = 0;
    std::string nombre;
    SDV sdv;
    double confianza = 40.0;
    double conocimiento = 20.0;
    double huella = 0.0;
    bool dentro = true;
    bool riesgo = false;
    std::string ultima = "esperar";
};

enum class Orden { Ninguna, Cooperar, Explorar, Descansar, Ayudar, Hablar, Salir };

struct Mundo {
    std::map<int, Persona> personas;
    std::mt19937_64 rng;
    unsigned long long semilla;
    int ciclo = 0;
    int comunidades = 1;
    int hijas = 0;
    int perdidas = 0;
    double comida = 80.0;
    double salud = 80.0;
    double conocimiento = 25.0;
    double ambiente = 85.0;
    double confianza = 42.0;
    double paz = 90.0;
    double bienestar = 0.0;
    double productividad = 0.0;
    double r = 0.0;
    double k = 0.0;
    double vhv = 0.0;
    double maxo = 0.0;
    int violaciones = 0;
    int derivas = 0;
    std::string problema = "ninguno";
    std::vector<std::string> historia;

    explicit Mundo(unsigned long long seed) : rng(seed), semilla(seed) {}

    double real(double a = 0.0, double b = 1.0) {
        return std::uniform_real_distribution<double>(a, b)(rng);
    }
    bool suerte(double p) { return std::bernoulli_distribution(p)(rng); }

    void iniciar() {
        for (int i = 1; i <= 11; ++i) {
            Persona p;
            p.id = i;
            p.nombre = (i == 1) ? "Max" : "Persona-" + std::to_string(i);
            p.sdv = {84.0, 72.0 + (i % 5), 70.0 + (i % 4)};
            p.confianza = 25.0 + (i % 6) * 2.0;
            p.conocimiento = 20.0 + (i % 4) * 3.0;
            personas[i] = p;
        }
        actualizar_indicadores();
    }

    void registrar(const std::string& s, bool viola = false) {
        std::ostringstream o;
        o << "[" << std::setw(3) << ciclo << "] " << s;
        historia.push_back(o.str());
        if (historia.size() > 250) historia.erase(historia.begin());
        if (viola) ++violaciones;
    }

    void avanzar(Orden orden_max = Orden::Ninguna, int objetivo = 0) {
        desgaste();
        if (ciclo > 0 && ciclo % 15 == 0) problema_aleatorio();

        for (auto& [id, p] : personas) {
            Orden orden = Orden::Ninguna;
            if (id == 1 && orden_max != Orden::Ninguna) orden = orden_max;
            decidir_y_actuar(p, orden, objetivo);
        }

        resolver_presiones();
        if ((ciclo + 1) % 10 == 0) instituciones();
        actualizar_indicadores();
        ++ciclo;
    }

    int personas_dentro() const {
        int n = 0;
        for (const auto& [id, p] : personas) if (p.dentro) ++n;
        return n;
    }

    int personas_riesgo() const {
        int n = 0;
        for (const auto& [id, p] : personas) if (p.riesgo && p.dentro) ++n;
        return n;
    }

    int personas_fuera() const {
        return static_cast<int>(personas.size()) - personas_dentro();
    }

private:
    void limitar() {
        auto clamp = [](double& x) { x = std::clamp(x, 0.0, 100.0); };
        clamp(comida); clamp(salud); clamp(conocimiento); clamp(ambiente);
        clamp(confianza); clamp(paz); clamp(bienestar); clamp(productividad);
    }

    void desgaste() {
        comida -= 0.10;
        salud -= 0.03;
        conocimiento -= 0.02;
        confianza -= 0.03;
        ambiente -= 0.02;
        paz -= 0.015;
        limitar();
    }

    void problema_aleatorio() {
        const int tipo = static_cast<int>(real(0, 4));
        if (tipo == 0) {
            comida -= 6;
            problema = "escasez de comida";
            registrar("hay una escasez de comida");
        } else if (tipo == 1) {
            salud -= 5;
            problema = "enfermedad";
            registrar("aparece una enfermedad");
        } else if (tipo == 2) {
            ambiente -= 5;
            problema = "danio ambiental";
            registrar("un danio ambiental golpea a la comunidad");
        } else {
            confianza -= 6;
            paz -= 5;
            problema = "conflicto";
            registrar("aparece un conflicto y sube la tension");
        }
        limitar();
    }

    void decidir_y_actuar(Persona& p, Orden manual, int objetivo) {
        if (!p.dentro) return;

        Orden orden = manual;
        if (orden == Orden::Ninguna) {
            const double r0 = real();
            const double agotamiento = 1.0 - p.sdv.promedio() / 100.0;
            if (r0 < 0.46 + 0.14 * (1.0 - agotamiento))
                orden = Orden::Cooperar;
            else if (r0 < 0.70)
                orden = Orden::Explorar;
            else if (r0 < 0.96)
                orden = Orden::Descansar;
            else
                orden = Orden::Salir;
        }

        p.ultima = texto(orden);

        if (orden == Orden::Salir) {
            p.dentro = false;
            registrar(p.nombre + " sale de la comunidad por decision propia");
            return;
        }

        if (orden == Orden::Cooperar) {
            p.sdv.sentido += 0.12;
            p.sdv.relacion += 0.16;
            p.sdv.cuerpo -= 0.06;
            p.huella += 1.0;
            vhv += 1.0;
            maxo += 0.10;
            comida += 0.04;
            confianza += 0.08;
            paz += 0.02;
            registrar(p.nombre + " coopera");
        } else if (orden == Orden::Explorar) {
            p.sdv.sentido += 0.32;
            p.sdv.relacion -= 0.05;
            p.huella += 0.5;
            vhv += 0.5;
            maxo += 0.04;
            conocimiento += 0.45;
            ambiente += 0.08;
            registrar(p.nombre + " explora una idea nueva");
        } else if (orden == Orden::Descansar) {
            p.sdv.cuerpo += 0.30;
            p.sdv.sentido -= 0.01;
            salud += 0.10;
            registrar(p.nombre + " descansa y recupera fuerzas");
        } else if (orden == Orden::Ayudar && objetivo > 0) {
            Persona* q = buscar(objetivo);
            if (q && q->dentro && q->id != p.id) {
                p.sdv.cuerpo -= 0.35;
                p.sdv.relacion += 0.08;
                q->sdv.cuerpo += 1.20;
                q->sdv.relacion += 0.60;
                q->sdv.sentido += 0.25;
                p.huella += 0.8;
                vhv += 0.8;
                comida += 0.35;
                confianza += 0.80;
                p.confianza = std::min(100.0, p.confianza + 4.0);
                q->confianza = std::min(100.0, q->confianza + 4.0);
                registrar(p.nombre + " ayuda a " + q->nombre);
            } else {
                registrar(p.nombre + " intenta ayudar, pero no encuentra a esa persona");
            }
        } else if (orden == Orden::Hablar && objetivo > 0) {
            Persona* q = buscar(objetivo);
            if (q && q->dentro && q->id != p.id) {
                p.sdv.relacion += 0.45;
                q->sdv.relacion += 0.45;
                p.sdv.cuerpo -= 0.08;
                q->sdv.cuerpo -= 0.04;
                p.confianza = std::min(100.0, p.confianza + 5.0);
                q->confianza = std::min(100.0, q->confianza + 5.0);
                confianza += 1.20;
                conocimiento += 0.35;
                registrar(p.nombre + " habla con " + q->nombre);
            } else {
                registrar(p.nombre + " intenta hablar, pero no encuentra a esa persona");
            }
        }

        p.sdv.cuerpo = std::max(0.0, p.sdv.cuerpo);
        p.sdv.relacion = std::max(0.0, p.sdv.relacion);
        p.sdv.sentido = std::max(0.0, p.sdv.sentido);
        p.riesgo = !p.sdv.en_piso();
        limitar();
    }

    Persona* buscar(int id) {
        auto it = personas.find(id);
        return it == personas.end() ? nullptr : &it->second;
    }

    static std::string texto(Orden o) {
        switch (o) {
            case Orden::Cooperar: return "cooperar";
            case Orden::Explorar: return "explorar";
            case Orden::Descansar: return "descansar";
            case Orden::Ayudar: return "ayudar";
            case Orden::Hablar: return "hablar";
            case Orden::Salir: return "salir";
            default: return "esperar";
        }
    }

    void resolver_presiones() {
        int coop = 0;
        for (const auto& [id, p] : personas)
            if (p.dentro && p.ultima == "cooperar") ++coop;

        salud += coop * 0.01;
        comida += coop * 0.015;
        paz += coop * 0.02;
    }

    void instituciones() {
        const int dentro = personas_dentro();
        if (dentro >= 7 && comida >= 45 && salud >= 55 && confianza >= 35 && suerte(0.13)) {
            ++comunidades;
            ++hijas;
            const int base = static_cast<int>(personas.size()) + 1;

            personas[base] = Persona{
                base, "Nueva-" + std::to_string(base),
                {76, 74, 72}, 35, 20, 0, true, false, "esperar"
            };
            personas[base + 1] = Persona{
                base + 1, "Nueva-" + std::to_string(base + 1),
                {76, 74, 72}, 35, 20, 0, true, false, "esperar"
            };
            registrar("nace una comunidad hija viable");
        }

        if (dentro > 0 && dentro <= 2 && suerte(0.20)) {
            ++perdidas;
            comunidades = std::max(0, comunidades - 1);
            registrar("una comunidad deja de poder mantenerse activa", true);
        }

        r = perdidas == 0 ? (hijas ? static_cast<double>(hijas) : 0.0)
                          : static_cast<double>(hijas) / static_cast<double>(perdidas);

        k = dentro + confianza / 20.0;

        derivas = 0;
        if (confianza < 25) ++derivas;
        if (personas_fuera() >= 5) ++derivas;
    }

    void actualizar_indicadores() {
        double sdv = 0.0;
        double rel = 0.0;
        int n = 0;
        int rel_n = 0;

        for (const auto& [id, p] : personas) {
            sdv += p.sdv.promedio();
            ++n;
            if (p.dentro) {
                rel += p.confianza;
                ++rel_n;
            }
        }

        const double promedio_sdv = n ? sdv / n : 0.0;
        const double confianza_personas = rel_n ? rel / rel_n : 0.0;

        confianza = 0.90 * confianza + 0.10 * confianza_personas;

        bienestar =
            0.35 * promedio_sdv +
            0.12 * comida +
            0.12 * salud +
            0.10 * conocimiento +
            0.10 * ambiente +
            0.10 * confianza +
            0.11 * paz;

        productividad =
            0.35 * conocimiento +
            0.25 * salud +
            0.20 * confianza +
            0.20 * ambiente;

        limitar();
    }
};

std::string barra(double x) {
    const int n = static_cast<int>(std::clamp(x, 0.0, 100.0) / 5.0);
    return std::string(n, '#') + std::string(20 - n, '.');
}

void mostrar_mundo(const Mundo& m) {
    int dentro = m.personas_dentro();
    int fuera = m.personas_fuera();
    int riesgo = m.personas_riesgo();

    double suma = 0.0;
    double minimo = 100.0;
    for (const auto& [id, p] : m.personas) {
        suma += p.sdv.promedio();
        minimo = std::min(minimo, p.sdv.promedio());
    }
    const double avg = m.personas.empty() ? 0.0 : suma / m.personas.size();

    std::cout
        << "
==============================================================
"
        << " MAXOCRACIA — ESTADO DEL MUNDO
"
        << "==============================================================
"
        << " ciclo " << m.ciclo
        << " | semilla " << m.semilla
        << " | comunidades " << m.comunidades
        << " | personas " << m.personas.size() << "

"

        << "PERSONAS
"
        << " dentro " << dentro
        << " | en riesgo " << riesgo
        << " | salieron " << fuera << "

"

        << std::fixed << std::setprecision(1)

        << "BIENESTAR
"
        << " SDV promedio " << std::setw(5) << avg << " [" << barra(avg) << "]
"
        << " SDV minimo   " << std::setw(5) << minimo << " [" << barra(minimo) << "]
"
        << " bienestar    " << std::setw(5) << m.bienestar << " [" << barra(m.bienestar) << "]
"
        << " paz          " << std::setw(5) << m.paz << " [" << barra(m.paz) << "]

"

        << "CONDICIONES DEL MUNDO
"
        << " comida       " << std::setw(5) << m.comida << " [" << barra(m.comida) << "]
"
        << " salud        " << std::setw(5) << m.salud << " [" << barra(m.salud) << "]
"
        << " conocimiento " << std::setw(5) << m.conocimiento << " [" << barra(m.conocimiento) << "]
"
        << " ambiente     " << std::setw(5) << m.ambiente << " [" << barra(m.ambiente) << "]
"
        << " confianza    " << std::setw(5) << m.confianza << " [" << barra(m.confianza) << "]
"
        << " productividad" << std::setw(5) << m.productividad << " [" << barra(m.productividad) << "]

"

        << "CRECIMIENTO
"
        << " R crecimiento " << std::setw(5) << m.r
        << " | K capacidad " << std::setw(5) << m.k << "
"
        << " hijas " << m.hijas
        << " | comunidades perdidas " << m.perdidas << "
"
        << " VHV (huella) " << std::setw(8) << m.vhv
        << " | Maxo " << std::setw(8) << m.maxo << "

"

        << "ULTIMO PROBLEMA: " << m.problema << "
"
        << "violaciones: " << m.violaciones
        << " | senales de deriva: " << m.derivas << "
";

    std::vector<std::string> vigilar;
    if (m.comida < 50) vigilar.push_back("comida");
    if (m.salud < 50) vigilar.push_back("salud");
    if (m.conocimiento < 50) vigilar.push_back("conocimiento");
    if (m.ambiente < 50) vigilar.push_back("ambiente");
    if (m.confianza < 50) vigilar.push_back("confianza");
    if (m.paz < 50) vigilar.push_back("paz");

    std::cout << "para vigilar: ";
    if (vigilar.empty()) {
        std::cout << "ninguna presion fuerte";
    } else {
        for (std::size_t i = 0; i < vigilar.size(); ++i) {
            if (i) std::cout << ", ";
            std::cout << vigilar[i];
        }
    }
    std::cout << "
";
}

void mostrar_personas(const Mundo& m) {
    std::cout
        << "
PERSONAS
"
        << "--------------------------------------------------------------
"
        << " id | nombre       | estado     | SDV | confianza | ultima
"
        << "--------------------------------------------------------------
";

    for (const auto& [id, p] : m.personas) {
        std::cout
            << std::setw(3) << id
            << " | " << std::setw(12) << std::left << p.nombre << std::right
            << " | " << std::setw(10)
            << (p.dentro ? (p.riesgo ? "en riesgo" : "dentro") : "salio")
            << " | " << std::setw(3) << std::setprecision(1) << p.sdv.promedio()
            << " | " << std::setw(9) << p.confianza
            << " | " << p.ultima << "
";
    }
}

void mostrar_historia(const Mundo& m) {
    std::cout
        << "
HISTORIA RECIENTE
"
        << "--------------------------------------------------------------
";

    const std::size_t inicio = m.historia.size() > 18 ? m.historia.size() - 18 : 0;
    for (std::size_t i = inicio; i < m.historia.size(); ++i)
        std::cout << m.historia[i] << '
';
}

bool numero(const std::string& s, int& out) {
    try {
        out = std::stoi(s);
        return true;
    } catch (...) {
        return false;
    }
}

void ayuda() {
    std::cout << R"(
COMANDOS
  mundo                      ver todas las estadisticas
  personas                   ver las personas
  historia                   ver lo que acaba de pasar
  avanzar N                  pasar N ciclos

  max cooperar               Max coopera
  max explorar               Max explora
  max descansar              Max descansa
  max ayudar ID              Max ayuda a una persona
  max hablar ID              Max habla con una persona
  max salir                  Max sale del compromiso

  ayuda                      esta ayuda
  salir                      cerrar el juego

Las decisiones de Max afectan el siguiente ciclo. Las demas personas
siguen viviendo y decidiendo por su cuenta.
)";
}

} // namespace maxo

int main() {
    using namespace maxo;

    Mundo mundo(42);
    mundo.iniciar();

    std::cout
        << "=== MAXOCRACIA ===
"
        << "Un pequeno mundo para experimentar con decisiones y consecuencias.
";

    ayuda();
    mostrar_mundo(mundo);

    Orden orden_pendiente = Orden::Ninguna;
    int objetivo_pendiente = 0;
    std::string linea;

    while (true) {
        std::cout << "
maxo> " << std::flush;
        if (!std::getline(std::cin, linea)) break;

        std::istringstream in(linea);
        std::string cmd, arg, extra;
        in >> cmd >> arg >> extra;

        for (char& c : cmd)
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        for (char& c : arg)
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));

        if (cmd == "salir" || cmd == "q") break;
        if (cmd == "ayuda" || cmd == "?") {
            ayuda();
            continue;
        }
        if (cmd == "mundo" || cmd == "d") {
            mostrar_mundo(mundo);
            continue;
        }
        if (cmd == "personas" || cmd == "p") {
            mostrar_personas(mundo);
            continue;
        }
        if (cmd == "historia" || cmd == "e") {
            mostrar_historia(mundo);
            continue;
        }

        if (cmd == "avanzar" || cmd == "n") {
            int n = 1;
            if (!arg.empty()) numero(arg, n);
            n = std::clamp(n, 1, 10000);

            for (int i = 0; i < n; ++i) {
                mundo.avanzar(orden_pendiente, objetivo_pendiente);
                orden_pendiente = Orden::Ninguna;
                objetivo_pendiente = 0;
            }

            mostrar_mundo(mundo);
            continue;
        }

        if (cmd == "max" || cmd == "m") {
            Orden o = Orden::Ninguna;

            if (arg == "cooperar" || arg == "c") o = Orden::Cooperar;
            else if (arg == "explorar" || arg == "x") o = Orden::Explorar;
            else if (arg == "descansar" || arg == "d") o = Orden::Descansar;
            else if (arg == "salir" || arg == "r") o = Orden::Salir;
            else if (arg == "ayudar" || arg == "a") o = Orden::Ayudar;
            else if (arg == "hablar" || arg == "h") o = Orden::Hablar;

            if (o == Orden::Ayudar || o == Orden::Hablar) {
                int id = 0;
                if (!extra.empty()) numero(extra, id);

                if (id <= 0) {
                    std::cout << "Usa: max " << arg << " ID
";
                } else {
                    orden_pendiente = o;
                    objetivo_pendiente = id;
                    std::cout << "Listo: esa accion ocurrira en el proximo ciclo.
";
                }
            } else if (o != Orden::Ninguna) {
                orden_pendiente = o;
                objetivo_pendiente = 0;
                std::cout << "Listo: esa accion ocurrira en el proximo ciclo.
";
            } else {
                std::cout << "No entendi esa orden. Escribe 'ayuda'.
";
            }

            continue;
        }

        std::cout << "No entendi. Escribe 'ayuda'.
";
    }

    return 0;
}
