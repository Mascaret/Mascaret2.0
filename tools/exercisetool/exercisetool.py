# Kivy libs import
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty

# Python libs import
import pandas as pd

# Personal libs import
from data.db import MyDB
from config.cursor import Cursor
from data.logicalobject.exercise import Exercise
from data.logicalobject.appexercise import AppExercise
from data.logicalobject.exercisescaling import ExerciseScaling
from data.logicalobject.exsctraining import ExScTraining
from data.logicalobject.training import Training
from data.logicalobject.workout import Workout
from data.logicalobject.series import Serie
from ressource.object.singleton import Singleton

from gui.widget.dtbobjctdropdown import DtbObjctDropDown

Builder.load_string('''
########################## Beginning of ExerciseTool ##########################

<ExerciseToolHP>:

<TrainingIntroLayout>:
    training_name_label: training_name_label
    training_type_label: training_type_label
    exercises: exercises
    Button:
        text: 'Begin'
        on_release: root.begin_workout()
        size_hint: None, None
        size: 100,50
        pos: 100,100
    Label:
        id: training_name_label
        text: 'training_name_label'
        size_hint: None, None
        size: 150,50
        pos: 100,600
    Label:
        id: training_type_label
        text: 'training_type_label'
        size_hint: None, None
        size: 150,50
        pos: 100,700
    StackLayout:
        id: exercises
        size_hint: None, None
        size: 300,400
        pos: 300,300
        canvas:
            Color:
                rgba: 1,0,0,1
            Rectangle:
                size: self.size
                pos: self.pos

<ExerciseScalingEditBox>:
    exsc_name_label: exsc_name_label
    series_n_input: series_n_input
    reps_n_input: reps_n_input
    size_hint: 1, None
    height: 60
    Label:
        size_hint: 1.6, 1
        id: exsc_name_label
        text: 'test'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            Label:
                size_hint: 1.6, 1
                text: 'Series: '
            TextInput:
                id: series_n_input
                text: '7'
        BoxLayout:
            Label:
                size_hint: 1.6, 1
                text: 'Reps: '
            TextInput:
                id: reps_n_input
                text: '7'

<WorkoutLayout>:


<AppExerciseLayout>:
    exercise_name_label: exercise_name_label
    exercise_pic_image: exercise_pic_image
    exercise_desc_label: exercise_desc_label
    exercise_rq_label: exercise_rq_label
    Label:
        id: exercise_name_label
    Image:
        id: exercise_pic_image
    Label:
        id: exercise_desc_label
    Label:
        id: exercise_rq_label

############################# End of ExerciseTool #############################
''')


class ExToolDtbContainer(metaclass=Singleton):

    def __init__(self, **kwargs):
        pass


class ExerciseTool(ScreenManager):

    def __init__(self, **kwargs):
        super(ExerciseTool, self).__init__(**kwargs)
        #init of the db
        self.mydb = MyDB()
        # init the dtf
        self.init_dtf()
        # gui building
        self.build_GUI()


    def build_GUI(self):
        self.homepage = ExerciseToolHP(self)
        self.add_widget(Screen(name = 'hpscreen'))
        self.get_screen('hpscreen').add_widget(self.homepage)

        self.trainingintrolayout = TrainingIntroLayout(self)
        self.add_widget(Screen(name = 'trainingintroscreen'))
        self.get_screen('trainingintroscreen').add_widget(self.trainingintrolayout)


    def init_dtf(self):
        # we get the list of favorites workout
        self.trainings_dataframe = self.mydb.get_dataframe(objct = Training)
        self.favtrainings_dataframe = self.trainings_dataframe[self.trainings_dataframe.training_fav == 1]
        # print(self.favtrainings_dataframe.head(n=1).index.item())

        self.workouts_dataframe = self.mydb.get_dataframe(objct = Workout)


    def get_wide(self):
    # This method must trigger the "fullpage" mode of the tool in mascaret
        # TO BE REPLACED BY A MODE (WIDE/NARROW) CHECK /B
        if self.to_window(*self.pos)[0] == 64:
            return
        else:
            print('go wide')
        # TO BE REPLACED BY A MODE (WIDE/NARROW) CHECK /E

    def show_training_intro(self, training_id):

        # dataframe of the exercises
        self.exercises_dataframe = self.mydb.get_dataframe(
                                            objct = Exercise,
                                            index = False
                                                     )
        # dataframe with the exsc
        exercisescalings_dataframe = self.mydb.get_dataframe(
                                            objct = ExerciseScaling,
                                            index = False
                                                            )
        # dataframe with the association exsc - training
        exsctrainings_dataframe = self.mydb.get_dataframe(
                                            objct = ExScTraining,
                                            index = False
                                                         )
        # we keep only the asso exsc - training related to the actual training
        exsctrainings_dataframe = exsctrainings_dataframe[
                            exsctrainings_dataframe.training_id == training_id
                                                         ]

        # dataframe with the workouts
        former_workouts_dataframe = self.mydb.get_dataframe(
                                            objct = Workout,
                                            index = False
                                                           )
        # we get the latest workout_id
        if not former_workouts_dataframe.empty:
        # if it is not our first workout:
            self.latest_workout_id = former_workouts_dataframe.workout_id.max()
            self.latest_appex_id = self.mydb.get_dataframe(
                                                objct = AppExercise,
                                                index = False
                                                             ).appexercise_id.max()
            self.latest_serie_id = self.mydb.get_dataframe(
                                                objct = Serie,
                                                index = False
                                                             ).serie_id.max()
        else:
        # if it is our first workout:
            # we init the ids and return
            self.latest_workout_id = 0
            self.latest_appex_id = 0
            self.latest_serie_id = 0

        # print('latest_workout_id: ' + str(self.latest_workout_id))

        # we keep only the workouts for the actual training
        former_workouts_dataframe = former_workouts_dataframe[
                                    former_workouts_dataframe.training_id
                                                    ==
                                                training_id
                                                             ]
        # if there are already workouts of the actual training
        if not former_workouts_dataframe.empty:
            # we get its informations
            self.latest_former_workout_serie = former_workouts_dataframe.ix[
                                former_workouts_dataframe.idxmax()['workout_n']
                                                                            ]
            # the number of the latest workout of the actual training
            self.latest_workout_n = self.latest_former_workout_serie.workout_id
            # dataframe with the series merged with their appex
            self.former_series_dataframe = pd.merge(
                self.mydb.get_dataframe(objct = Serie, index = False),
                self.mydb.get_dataframe(objct = AppExercise, index = False),
                how = 'left',
                on = 'appexercise_id'
                                                   )
            # we keep only the series of the latest workout of the actual
            # training
            self.former_series_dataframe = self.former_series_dataframe[
                                self.former_series_dataframe.workout_id
                                                    ==
                                        self.latest_workout_n
                                                                       ]
        else:
            self.latest_workout_n = 0

        print('latest_workout_n: ' + str(self.latest_workout_n))

        # dataframe with the exsc for the actual training sorted
        self.current_exercisescalings_dataframe = pd.merge(
                                    pd.merge(
                                        exsctrainings_dataframe,
                                        exercisescalings_dataframe,
                                        how = 'left',
                                        on = 'exercisescaling_id'
                                            ),
                                    exercises_dataframe,
                                    how = 'left',
                                    on = 'exercise_id'
                                                          ).sort(
                                                columns = 'exercisescaling_n'
                                                                )



        self.trainingintrolayout.init_training(training_id)

        self.current = 'trainingintroscreen'


class ExerciseToolHP(RelativeLayout):

    def __init__(self, maintool, **kwargs):
        super(ExerciseToolHP, self).__init__(**kwargs)
        # ref of the maintool
        self.maintool = maintool
        # gui
        self.build_GUI()

    def choose_workout_dpd(self):
        pass

    def build_GUI(self):
        self.workoutchoice_btn = DtbObjctDropDown(
                linked_dataframe = self.maintool.favtrainings_dataframe,
                objct_id = self.maintool.favtrainings_dataframe.head(
                                                            n=1).index.item(),
                attr_displayed_list = ['training_name'],
                size_hint = (None,None),
                size = (200,100),
                y = "500dp",
                x = "400dp"
                                                )
        self.go_btn = Button(
                text = 'GO',
                size_hint = (None,None),
                size = (100,100),
                on_release = self.launch_training,
                y = "500dp",
                x = "601dp"
                            )

        self.add_widget(self.workoutchoice_btn)
        self.add_widget(self.go_btn)


    def launch_training(self, instance):
        self.maintool.get_wide()
        self.maintool.show_training_intro(self.workoutchoice_btn.objct_id)




class ExerciseScalingEditBox(BoxLayout):

    exsc_name_label = ObjectProperty(None)

    series_n_input = ObjectProperty(None)

    reps_n_input = ObjectProperty(None)

    def __init__(self, exercisescaling_id, maintool, **kwargs):
        super(ExerciseScalingEditBox, self).__init__(**kwargs)
        # init of the exsc id
        self.exercisescaling_id = exercisescaling_id
        # ref of the maintool
        self.maintool = maintool
        # GUI building
        self.build_GUI()


    def init_exsc_name(self):
    # display the name of the exercise inthe appropriate label
        self.exsc_name_label.text = self.get_exsc_attr('exercise_name')

    def init_series_n_input(self, number):
    # display the name of the exercise inthe appropriate label
        self.series_n_input.text = str(number)

    def init_reps_n_input(self, number):
    # display the name of the exercise inthe appropriate label
        self.reps_n_input.text = str(number)


    def define_series_reps_n(self):
        # NEED TO BE REVIEWD!!!!

        # if it is the first time we do this training
        if self.maintool.latest_workout_n == 0:
            new_number_of_reps = self.get_exsc_attr('reps_min')
            new_number_of_series = self.get_exsc_attr('series_min')
        else:

            last_series = self.maintool.former_series_dataframe[
                            self.maintool.former_series_dataframe.exercise_id
                                                    ==
                                    self.get_exsc_attr('exercise_id')
                                                               ]
            last_series_goal = last_series.head(1).series_goal.item()

            last_reps_goal = last_series.head(1).reps_goal.item()

            # to get the results of last workout
            # last_series_number = len(last_series.index)
            last_reps_number = last_series.reps_qty.sum()

            if last_series_goal * last_reps_goal == last_reps_number:
            # it means that we fulfilled the goal in number of reps
            # therefore we need to increase goals

                # we first check if we have to increase the reps or the series
                if self.get_exsc_attr('series_reps_priority') == 'reps':
                # if the reps have the priority
                    if last_reps_goal == self.get_exsc_attr('reps_max'):
                    # if we are already at the max of the reps number
                        # we increase the number of series
                        new_number_of_series = min(
                        last_series_goal + self.get_exsc_attr('series_scalingrule'),
                        self.get_exsc_attr('series_max')
                                                  )
                        # and keep the number of reps at its max
                        new_number_of_reps = last_reps_goal
                    else:
                    # if we can increase the number of reps
                        # we keep the number of series as it is
                        new_number_of_series = last_series_goal
                        # and increase the number of reps
                        new_number_of_reps = min(
                        last_reps_goal + self.get_exsc_attr('reps_scalingrule'),
                        self.get_exsc_attr('reps_max')
                                                )
                else:
                # if the series have the priority
                    if last_series_goal == self.get_exsc_attr('series_max'):
                    # if we are already at the max of the series number
                        # we keep the number of series at its max
                        new_number_of_series = last_series_goal
                        # and increase the number of reps
                        new_number_of_reps = min(
                        last_reps_goal + self.get_exsc_attr('reps_scalingrule'),
                        self.get_exsc_attr('reps_max')
                                                  )
                    else:
                    # if we can increase the number of series
                        # we increase the number of series
                        new_number_of_series = min(
                        last_series_goal + self.get_exsc_attr('series_scalingrule'),
                        self.get_exsc_attr('reps_max')
                                                  )
                        # and keep the number of reps as it is
                        new_number_of_reps = last_reps_goal

            else:
            # it means that we didn't fulfill the goal in number of reps
                new_number_of_reps = last_reps_goal
                # therefore we need to keep the same goals
                new_number_of_series = last_series_goal

        return [new_number_of_series, new_number_of_reps]


    def get_exsc_attr(self, attr):
    # this method get the exsc attr in the dtf
        return self.maintool.current_exercisescalings_dataframe.loc[
                                                    self.exercisescaling_id,
                                                    attr
                                                                   ]

    def build_GUI(self):
        print('building gui of exc item')
        # we get the name of the ex and display it
        self.init_exsc_name()
        # we get the goals we should try to achieve
        exercise_goals = self.define_series_reps_n()
        # and display them
        self.init_series_n_input(exercise_goals[0])
        self.init_reps_n_input(exercise_goals[1])

    def get_series_n_input(self):
        return int(self.series_n_input.text)

    def get_reps_n_input(self):
        return int(self.reps_n_input.text)

    def get_appex_serie(self, workout_id, appex_id):

        return pd.Series({
        'appexercise_id': appex_id,
        'exercise_id': self.get_exsc_attr('exercise_id'),
        'workout_id': workout_id,
        'rep_time': self.get_exsc_attr('rep_time'),
        'rec_time': self.get_exsc_attr('rec_time'),
        'series_goal': self.get_series_n_input(),
        'reps_goal': self.get_reps_n_input()
                        })

    def get_series_dtf(self, first_serie_id, appex_id):

        print('!!!!!!!!!!!!!!!!!!!!! seriedtf !!!!!!!!!!!!!!!!!!!!!!!')


        serie_id = first_serie_id

        print('serie_id: ' + str(serie_id))

        series_dtf = pd.DataFrame(columns =
                                            [
                                            "serie_id", "appexercise_id",
                                            "serie_n", "reps_qty"
                                            ]
                                 )

        for serie_n in range(self.get_series_n_input()):

            series_dtf = series_dtf.append(pd.Series({
                "serie_id": serie_id,
                "appexercise_id": appex_id,
                "serie_n": serie_n + 1,
                "reps_qty": 0
                                                    }), ignore_index = True)
            serie_id += 1


        print('series_dtf:')
        print(series_dtf)
        print('!!!!!!!!!!!!!!!!!!!!! seriedtf !!!!!!!!!!!!!!!!!!!!!!!')

        return(series_dtf)

class TrainingIntroLayout(RelativeLayout):
    training_name_label = ObjectProperty()

    training_type_label = ObjectProperty()

    exercises = ObjectProperty()

    def __init__(self, maintool, **kwargs):
        super(TrainingIntroLayout, self).__init__(**kwargs)
        # ref of the maintool
        self.maintool = maintool
        # init of the exercisescaling_items_dict
        self.exercisescaling_items_dict = {}
        # gui
        self.build_GUI()


    def add_exercise_scaling_edit_box(self, exercisescaling_id):
    # this method create an exercisescaling item, enabling us to
    # choose our goals for the workout
        # creaion and ref of the exercisescaling item
        self.exercisescaling_items_dict[exercisescaling_id] = (
        ExerciseScalingEditBox(
                            exercisescaling_id = exercisescaling_id,
                            maintool = self.maintool
                              )
                                                              )
        # adding of it in the box of exercises
        self.exercises.add_widget(
                self.exercisescaling_items_dict[exercisescaling_id]
                                 )


    def init_training_name(self):
    # update the name of the training
        self.training_name_label.text = self.get_training_attr('training_name')

    # def update_training_desc(self):
    # # update the desc of the training
    #     self.training_name_label.text = self.get_training_attr('training_desc')

    def init_exercisescalings(self):
    # this method launch the creation of an exercisescaling item for each ex
    # of the workout
        # for each exercise
        for exercisescaling_id in self.maintool.current_exercisescalings_dataframe.index:
            # launch of the method creating the object
            self.add_exercise_scaling_edit_box(exercisescaling_id)

    def get_training_attr(self, attr):
    # this method get the training attr in the dtf
        return self.maintool.trainings_dataframe.loc[self.training_id, attr]

    def begin_workout(self):

        print('workout_serie: ')
        print(self.get_workout_serie())

        self.get_appex_and_series_dataframes()

        print('lets begin')

    def build_GUI(self):
        pass

    def init_training(self, training_id):
        self.training_id = training_id

        self.init_training_name()

        # self.update_training_desc()

        self.init_exercisescalings()

    def get_workout_serie(self):
    # this method creates and returns the workout serie
        return pd.Series({
        "workout_id": self.maintool.latest_workout_id + 1,
        "workout_date": "01/12/2015",
        "workout_n": self.maintool.latest_workout_n + 1,
        "training_id": self.training_id
                                       })


    def get_appex_and_series_dataframes(self):
    # this method creates and returns the appex dtf and the series dtf
        # init the appex dtf
        appex_dataframe = pd.DataFrame(columns = [
        "appexercise_id", "exercise_id",
        "workout_id", "rep_time",
        "rec_time", "series_goal",
        "reps_goal"
                                                 ]
                                      )
        # init the series dtf
        series_dataframe = pd.DataFrame(columns = [
        "serie_id", "appexercise_id",
        "serie_n", "reps_qty"
                                                 ]
                                      )
        # get the first ids we need to use
        first_serie_id = self.maintool.latest_serie_id + 1
        first_appex_id = self.maintool.latest_appex_id + 1

        # for each appex item in the layout
        for appex_item in self.exercisescaling_items_dict.values():
            # we get the appex infrmation and add them to the appex dtf
            appex_dataframe = appex_dataframe.append(
                    appex_item.get_appex_serie(
                            workout_id = self.maintool.latest_workout_id + 1,
                            appex_id = first_appex_id
                                              ),
                    ignore_index = True
                                                    )

            # we get the series info and add them in the series dtf
            series_dataframe = series_dataframe.append(
                    appex_item.get_series_dtf(
                            first_serie_id = first_serie_id,
                            appex_id = first_appex_id
                                              ),
                    ignore_index = True
                                                    )

            first_appex_id += 1
            first_serie_id = series_dataframe.serie_id.max() + 1

        print('appex_dataframe: ')
        print(appex_dataframe)

        print('series_dataframe: ')
        print(series_dataframe)



class WorkoutLayout(RelativeLayout):
    pass


class AppExerciseLayout(RelativeLayout):

    exercise_name_label = ObjectProperty()

    exercise_pic_image = ObjectProperty()

    exercise_desc_label = ObjectProperty()

    exercise_rq_label = ObjectProperty()

    def __init__(self, maintool, **kwargs):
        super(AppExerciseLayout, self).__init__(**kwargs)
        self.maintool = maintool

    def update_appex_id(self, appex_id):
        self.appex_id = appex_id

        self.exercise_id = self.get_appex_attr('exercise_id')

    def update_exercise_name(self):
    # this methode upste the name displayed in the layout
        self.exercise_name_label.text = self.get_exercise_attr('exercise_name')

    def update_exercise_pic(self):
    # this methode upste the pic displayed in the layout
        pass

    def update_exercise_desc(self):
    # this methode upste the desc displayed in the layout
        self.exercise_desc_label.text = self.get_exercise_attr('exercise_desc')

    # def update_exercise_rq(self):
    #     pass

    def get_appex_attr(self, attr):
    # this method get the appex attr in the dtf
        return self.maintool.current_appex_dataframe.loc[
                                                    self.appex_id,
                                                    attr
                                                        ]

    def get_exercise_attr(self, attr):
    # this method get the exercise attr in the dtf
        return self.maintool.exercises_dataframe.loc[
                                                    self.exercise_id,
                                                    attr
                                                    ]


class Timer():
    pass
