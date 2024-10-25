from connections import WS


import blueprints.users as users
import blueprints.fragments as fragments
import blueprints.milestones as milestones
users.register_callbacks()
fragments.register_callbacks()
milestones.register_callbacks()


if __name__ == '__main__':
    WS.start(thread=True)
    WS.waitThread()
